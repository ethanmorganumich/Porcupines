import SwiftUI

final class UserState : ObservableObject {
    @Published var view: String;
    @Published var previous_view: String;
    @Published var note_idx: Int;

    static let shared = UserState()
    private init() {
        self.view = ""
        self.previous_view = ""
        self.note_idx = -1
    }
    private let serverUrl = "https://us-central1-notesmart.cloudfunctions.net/"
    @Published private(set) var notes = [Note]()
    private let nFields = Mirror(reflecting: Note()).children.count
    
    func getNotes() {
        guard let apiUrl = URL(string: serverUrl+"notes/") else {
            print("getNotes: Bad URL")
            return
        }

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
                for (note_idx, noteEntry) in notesReceived.enumerated() {
                    let tag_data = noteEntry["metadata"] as? [[String:Any]] ?? []
                    var tags_list = []
                    for tag_item in tag_data.enumerated() {
                        tags_list.append((tag_item.element["name"]) as! String)
                    }
                        self.notes.append(Note(title: (noteEntry["title"] as? String) ?? "",
                                               text: (noteEntry["content"] as! String),
                                               timestamp: "timestamp",
                                               idx: note_idx,
                                               id: (noteEntry["note_id"] as! String),
                                               tags: (tags_list as! [String])
                                              ))
                }
            }
        }.resume()
    }
    
    func viewNote(_ idx: Int) {
        note_idx = idx
        previous_view = view
        view = "preview note view"//"existing note view"
    }
    
    func saveNote(_ note: Note, _ updated_title: String, _ updated_content: String) {
        let jsonObj = ["title": updated_title,
                       "content": updated_content]
        
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
                       "content": content]
        
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
        
        guard let apiUrl = URL(string: serverUrl+"notes/"+self.notes[self.note_idx].id!) else {
            print("deleteNote: Bad URL")
            return
        }
        
        var request = URLRequest(url: apiUrl)
        request.setValue("application/json; charset=utf-8", forHTTPHeaderField: "Content-Type")
        request.httpMethod = "DELETE"
        
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

    func createUser(_ email: String, _ password: String){
        let jsonObj = ["email": email,
                        "password": password]
        
        guard let jsonData = try? JSONSerialization.data(withJSONObject: jsonObj) else {
            print("saveNote: jsonData serialization error")
            return
        }

        guard let apiUrl = URL(string: serverUrl+"users/") else {
            print("createUser: Bad URL")
            return
        }

        var request = URLRequest(url: apiUrl)
        request.setValue("application/json; charset=utf-8", forHTTPHeaderField: "Accept")
        request.httpMethod = "POST"
        request.httpBody = jsonData
        
        // dont care about response
    }

    func signIn(_ email: String, _ password: String){
        let jsonObj = ["email": email,
                        "password": password]
        
        guard let jsonData = try? JSONSerialization.data(withJSONObject: jsonObj) else {
            print("saveNote: jsonData serialization error")
            return
        }

        guard let apiUrl = URL(string: serverUrl+"users/") else {
            print("getUser: Bad URL")
            return
        }

        var request = URLRequest(url: apiUrl)
        request.setValue("application/json; charset=utf-8", forHTTPHeaderField: "Accept")
        request.httpMethod = "GET"
        request.httpBody = jsonData
        
        // needs logic to get access_token from response
    }
}
