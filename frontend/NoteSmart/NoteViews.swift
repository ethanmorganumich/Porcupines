//
//  NewNoteView.swift
//  NoteSmart
//
//  Created by Sam Jaehnig on 11/4/22.
//

import SwiftUI
import MarkdownUI

struct NewNoteView: View {
    
    @ObservedObject var user_state = UserState.shared
    
    @State var note_title: String = "Note title...";
    @State var note_content: String = "start writing...";
    
    var body: some View {
        VStack {
            VStack{
                HStack {
                    if(!user_state.trial_demo) {
                        SaveBackButton(note_title: $note_title, note_content: $note_content, close_action: "create")
                    }
                    Spacer()
                    if(user_state.trial_demo) {
                        TrialDemoSaveButton(action: {
                            user_state.trial_demo_note["note_title"] = note_title
                            user_state.trial_demo_note["note_content"] = note_content
                        })
                    }
                }
                NoteEditor(note_title: $note_title, note_content: $note_content)
                Spacer()
            }
        }
    }
}

struct PreviewNoteView: View {
    @ObservedObject var user_state = UserState.shared
    
    @State var note_title: String = "";
    @State var note_content: String = "";
    
    var body: some View {
        VStack {
            VStack {
                HStack {
                    SimpleBackButton()
                    Spacer()
                }
                if let note = user_state.note_viewed {
                    VStack (alignment: .leading){
                        Text(note_title)
                            .lineLimit(1)
                            .frame(height: 40)
                            .padding([.leading], 3)
                            .padding([.bottom], 25)
                            .font(Font.custom("Inter-SemiBold", size: 25))
                        ScrollView(.vertical){
                            Markdown(note_content)
                                .padding([.leading, .trailing], 15)
                                .padding([.top, .bottom], 15)
                                .background(Color("grey"), in: RoundedRectangle(cornerRadius: 10))
                        }
                        .frame(height: 500)
                    }
                    .onTapGesture { user_state.view = "existing note view" }
                    .onAppear {
                        note_content = note.text!
                        note_title = note.title!
                    }
                    .frame(width: 300, alignment: .leading)
                    .padding(.leading, 5)
                    Spacer()
                }
                Spacer()
                TagList()
            }
        }
    }
    
}

struct ExistingNoteView: View {
    @ObservedObject var user_state = UserState.shared
    
    @State var note_title: String = "";
    @State var note_content: String = "";
    @State var note_details_showing: Bool = false;
    
    var body: some View {
        VStack {
            VStack {
                HStack {
                    SaveBackButton(note_title: $note_title, note_content: $note_content, close_action: "save")
                    Spacer()
                    DeleteNoteButton()
                }
                if let note = user_state.note_viewed {
                    NoteEditor(note_title: $note_title, note_content: $note_content)
                        .onAppear() {
                            note_content = note.text!
                            note_title = note.title!
                        }
                }
                Spacer()
                TagList()
            }
        }
    }
}

struct NoteEditor: View {
    @ObservedObject var user_state = UserState.shared
    
    @Binding var note_title: String;
    @State var note_edited: String = "timestamp";
    @Binding var note_content: String;
    @State var placeholder_title: Bool = true;
    @State var placeholder_content: Bool = true;
    
    var body: some View {
        VStack {
            TextEditor(text: $note_title)
                .font(Font.custom("Inter-SemiBold", size: 25))
                .lineLimit(1)
                .frame(height: 40)
                .onTapGesture {
                    if(user_state.view == "new note view" && placeholder_title) {
                        note_title = ""
                        placeholder_title = false
                    }
                }
                .padding([.bottom], 25)
                .autocapitalization(.none)
            GeometryReader { geometry in
                ScrollView(.vertical){
                    TextEditor(text: $note_content)
                        .font(Font.custom("Inter-Regular", size: 15))
                        .onTapGesture {
                            if(user_state.view == "new note view" && placeholder_content) {
                                note_content = ""
                                placeholder_content = false
                            }
                        }
                        .autocapitalization(.none)
                        .frame(minHeight: 500)
                }
                .frame(minHeight: 500)
            }
        }
        .frame(width: 300)
    }
}

struct TrialDemoSaveButton: View {
    @ObservedObject var user_state = UserState.shared
    var action: () -> Void
    
    var body: some View {
        HStack {
            Spacer()
            Button(action: {
                action()
                user_state.view = "sign-up view"
            }) {
                Image(systemName: "checkmark.circle")
                    .font(.system(size: 30))
                    .foregroundColor(Color("blue70"))
            }
            
            .padding(.bottom, 50)
            .padding(.trailing, 25)
        }
    }
}

struct SaveBackButton: View {
    @Binding var note_title: String;
    @Binding var note_content: String;
    @ObservedObject var user_state = UserState.shared
    var close_action: String;
    
    var body: some View {
        HStack {
            Button(action: {
                user_state.view = user_state.previous_view
                if(close_action == "save") { user_state.saveNote(user_state.note_viewed, note_title, note_content)}
                else {
                    user_state.createNote(note_title, note_content)
                }
            }) {
                Image(systemName: "chevron.backward.circle")
                    .font(.system(size: 30))
                    .foregroundColor(Color("blue70"))
            }
            .padding(.bottom, 50)
            .padding(.leading, 25)
            Spacer()
        }
    }
}

struct SimpleBackButton: View {
    @ObservedObject var user_state = UserState.shared
    
    var body: some View {
        HStack {
            Button(action: {
                user_state.view = user_state.previous_view
            }) {
                Image(systemName: "chevron.backward.circle")
                    .font(.system(size: 30))
                    .foregroundColor(Color("blue70"))
            }
            .padding(.bottom, 50)
            .padding(.leading, 25)
            Spacer()
        }
    }
}


struct DeleteNoteButton: View {
    @ObservedObject var user_state = UserState.shared
    
    var body: some View {
        Button(action: {
            user_state.deleteNote()
            user_state.view = user_state.previous_view
        }) {
            Image(systemName: "trash")
                .font(.system(size: 30))
                .foregroundColor(Color("blue70"))
        }
        .padding(.bottom, 50)
        .padding(.trailing, 25)
    }
}

struct TagList: View {
    @ObservedObject var user_state = UserState.shared
    
    var body: some View {
        GeometryReader { geometry in
            VStack{
                Spacer()
                ScrollView(.horizontal){
                    HStack {
                        if let tags = user_state.filterTagMatches(false, "", user_state.note_viewed.tags!) {
                            ForEach(tags.indices, id: \.self) {
                                TagItem(tag: tags[$0])
                            }
                        }
                    }
                    .padding(.bottom, 10)
                    .padding([.leading, .trailing], 20)
                    .frame(minWidth: geometry.size.width)
                }
            }
        }
    }
}

struct TagItem: View {
    @ObservedObject var user_state = UserState.shared
    var tag: Tag;
    
    var body: some View {
        Text(tag.text!)
            .font(Font.custom("Inter-Regular", size: 15))
            .foregroundColor(.black)
            .padding([.top, .bottom], 5)
            .padding([.leading, .trailing], 15)
            .background(Color("grey"), in: RoundedRectangle(cornerRadius: 10))
            .onTapGesture {
                user_state.tag_viewed = tag
                user_state.view = "tag view"
            }
    }
}

