import SwiftUI

final class UserState : ObservableObject {
    @Published var view: String
    @Published var previous_view: String
    @Published var trial_demo: Bool
    @Published var tag_viewed: Tag
    @Published var note_viewed: Note
    @Published var access_token: String
    @Published var refresh_token: String
    @Published var email: String
    @Published var trial_demo_note: [String: String]
    
    static let shared = UserState()
    private init() {
        self.view = ""
        self.previous_view = ""
        self.trial_demo = false
        self.tag_viewed = Tag(text: "")
        self.note_viewed = Note(title: "", text: "", id: "", tags: [Tag]())
        self.access_token = ""
        self.refresh_token = ""
        self.email = ""
        self.trial_demo_note = [:]
    }
    private let serverUrl = "https://us-central1-notesmart.cloudfunctions.net/"
    @Published private(set) var notes = [Note]()
    @Published private(set) var tags = [Tag]()
    private let nFields = Mirror(reflecting: Note()).children.count
    
    func auth() -> String {
        return ";access_token="+self.access_token+";refresh_token="+refresh_token+";?#"
    }
    
    func getNotes() {
        guard let apiUrl = URL(string: serverUrl+"notes/" + self.auth()) else {
            print("getNotes: Bad URL")
            return
        }
        print(apiUrl)
        
        var request = URLRequest(url: apiUrl)
        request.setValue("application/json; charset=utf-8", forHTTPHeaderField: "Accept")
        request.httpMethod = "GET"
        
        URLSession.shared.dataTask(with: request) { data, response, error in
            
            guard let data = data, error == nil else {
                print("getNotes: NETWORKING ERROR")
                return
            }
            if let httpStatus = response as? HTTPURLResponse, httpStatus.statusCode != 200 {
                print("getNotes: HTTP STATUS: \(httpStatus.statusCode)")
                return
            }
            
            guard let jsonObj = try? JSONSerialization.jsonObject(with: data) as? [String:Any] else {
                print("getNotes: failed JSON deserialization")
                return
            }
            
            let notesReceived = jsonObj["notes"] as? [[String:Any]] ?? []
            DispatchQueue.main.async {
                self.notes = [Note]()
                self.tags = [Tag]()
                for (_, noteEntry) in notesReceived.enumerated() {
                    let tag_data = noteEntry["tags"] as? [String] ?? []
                    var tags_list = [Tag]()
                    for tag_item in tag_data.enumerated() {
                        let tag = Tag(text: tag_item.element)
                        tags_list.append(tag)
                        self.tags.append(tag)
                    }
                    
                    self.notes.append(Note(title: (noteEntry["title"] as? String) ?? "",
                                           text: (noteEntry["content"] as! String),
                                           id: (noteEntry["note_id"] as! String),
                                           tags: (tags_list as [Tag])
                                          ))
                }
            }
        }.resume()
    }
    
    
    func viewNote(_ id: String) {
        previous_view = view
        view = "preview note view"
        
        for note in self.notes {
            if(note.id == id) {
                self.note_viewed = note
                break
            }
        }
        
    }
    
    func saveNote(_ note: Note, _ updated_title: String, _ updated_content: String) {
        let jsonObj = ["title": updated_title,
                       "content": updated_content,
                       "access_token": self.access_token,
                       "refresh_token": self.refresh_token]
        
        guard let jsonData = try? JSONSerialization.data(withJSONObject: jsonObj) else {
            print("saveNote: jsonData serialization error")
            return
        }
        
        guard let apiUrl = URL(string: serverUrl+"notes/"+note.id!) else {
            print("saveNote: Bad URL")
            return
        }
        
        var request = URLRequest(url: apiUrl)
        request.setValue("application/json; charset=utf-8", forHTTPHeaderField: "Content-Type")
        request.httpMethod = "POST"
        request.httpBody = jsonData
        
        URLSession.shared.dataTask(with: request) { data, response, error in
            guard let _ = data, error == nil else {
                print("saveNote: NETWORKING ERROR")
                return
            }
            if let httpStatus = response as? HTTPURLResponse {
                if httpStatus.statusCode != 200 {
                    print("saveNote: HTTP STATUS: \(httpStatus.statusCode)")
                    return
                } else {
                    self.getNotes()
                }
            }
        }.resume()
    }
    
    func createNote(_ title: String, _ content: String) {
        let jsonObj = ["title": title,
                       "content": content,
                       "access_token": self.access_token,
                       "refresh_token": self.refresh_token]
        
        guard let jsonData = try? JSONSerialization.data(withJSONObject: jsonObj) else {
            print("createNote: jsonData serialization error")
            return
        }
        
        guard let apiUrl = URL(string: serverUrl+"notes/") else {
            print("createNote: Bad URL")
            return
        }
                
        var request = URLRequest(url: apiUrl)
        request.setValue("application/json; charset=utf-8", forHTTPHeaderField: "Content-Type")
        request.httpMethod = "POST"
        request.httpBody = jsonData
        
        URLSession.shared.dataTask(with: request) { data, response, error in
            guard let _ = data, error == nil else {
                print("createNote: NETWORKING ERROR")
                return
            }
            if let httpStatus = response as? HTTPURLResponse {
                if httpStatus.statusCode != 200 {
                    print("createNote: HTTP STATUS: \(httpStatus.statusCode)")
                    return
                } else {
                    self.getNotes()
                }
            }
        }.resume()
    }
    
    func deleteNote() {
        let jsonObj = ["access_token": self.access_token,
                       "refresh_token": self.refresh_token]
        
        guard let apiUrl = URL(string: serverUrl+"notes/"+self.note_viewed.id!) else {
            print("deleteNote: Bad URL")
            return
        }
        
        guard let jsonData = try? JSONSerialization.data(withJSONObject: jsonObj) else {
            print("createNote: jsonData serialization error")
            return
        }
                
        var request = URLRequest(url: apiUrl)
        request.setValue("application/json; charset=utf-8", forHTTPHeaderField: "Content-Type")
        request.httpMethod = "DELETE"
        request.httpBody = jsonData
        
        URLSession.shared.dataTask(with: request) { data, response, error in
            guard let _ = data, error == nil else {
                print("deleteNote: NETWORKING ERROR")
                return
            }
            if let httpStatus = response as? HTTPURLResponse {
                if httpStatus.statusCode != 200 {
                    print("deleteNote: HTTP STATUS: \(httpStatus.statusCode)")
                    return
                } else {
                    self.getNotes()
                }
            }
        }.resume()
    }
    
    func searchTagMatch(_ search: String, _ tags: [Tag]) -> Bool {
        for tag_elem in tags.enumerated() {
            let tag = tag_elem.element
            if(tagMatch(search, tag)) {
                return true;
            }
        }
        return false
    }
    
    func tagMatch(_ search: String, _ tag: Tag) -> Bool {
        let text = tag.text!
        if(search.count > text.count || search == "") {
            return false
        }
        let idx = text.index(text.startIndex, offsetBy: search.count - 1)
        if(search.lowercased() == text[...idx].lowercased()) {
            return true
        }
        
        return false
    }
    
    func filterTagMatches(_ searchFilter: Bool = true, _ search: String = "", _ tags: [Tag]) -> [Tag] {
        var curr_tags = [Tag]()
        var curr_tag_texts = [String]()
        for tag in tags {
            if((!searchFilter || self.tagMatch(search, tag)) && !curr_tag_texts.contains(tag.text!)) {
                curr_tags.append(tag)
                curr_tag_texts.append(tag.text!)
            }
        }
        return curr_tags
    }
    
    func signIn(_ email: String, _ password: String) {

        guard let apiUrl = URL(string: serverUrl+"authentication/;email="+email+";password="+password+";?#") else {
            print("signIn: Bad URL")
            return
        }

        var request = URLRequest(url: apiUrl)
        request.setValue("application/json; charset=utf-8", forHTTPHeaderField: "Accept")
        request.httpMethod = "GET"

        URLSession.shared.dataTask(with: request) { data, response, error in

            guard let data = data, error == nil else {
                print("signIn: NETWORKING ERROR")
                return
            }
            if let httpStatus = response as? HTTPURLResponse, httpStatus.statusCode != 200 {
                print("signIn: HTTP STATUS: \(httpStatus.statusCode)")
                return
            }
            
            guard let jsonObj = try? JSONSerialization.jsonObject(with: data) as? [String:Any] else {
                print("signIn: failed JSON deserialization")
                return
            }
            DispatchQueue.main.async {
                self.access_token = jsonObj["access_token"] as? String ?? ""
                self.refresh_token = jsonObj["refresh_token"] as? String ?? ""
                self.view = "home view"
                self.email = email
                if(self.trial_demo) {
                    self.createNote(self.trial_demo_note["note_title"]!, self.trial_demo_note["note_content"]!)
                    self.trial_demo = false
                }
            }
        }.resume()
    }
    
    func signUp(_ email: String, _ password: String) {
        let jsonObj = ["email": email,
                       "password": password]
        
        guard let jsonData = try? JSONSerialization.data(withJSONObject: jsonObj) else {
            print("signUp: jsonData serialization error")
            return
        }
        
        guard let apiUrl = URL(string: serverUrl+"authentication/") else {
            print("signUp: Bad URL")
            return
        }
        
        var request = URLRequest(url: apiUrl)
        request.setValue("application/json; charset=utf-8", forHTTPHeaderField: "Content-Type")
        request.httpMethod = "POST"
        request.httpBody = jsonData
        
        URLSession.shared.dataTask(with: request) { data, response, error in
            guard let _ = data, error == nil else {
                print("signUp: NETWORKING ERROR")
                return
            }
            if let httpStatus = response as? HTTPURLResponse {
                if httpStatus.statusCode != 200 {
                    print("signUp: HTTP STATUS: \(httpStatus.statusCode)")
                    DispatchQueue.main.async {
                        // tell user to authenticate email
                    }
                    return
                } else {
                    self.signIn(email, password)
                }
            }
        }.resume()
    }
}
