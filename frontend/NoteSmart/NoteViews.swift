//
//  NewNoteView.swift
//  NoteSmart
//
//  Created by Sam Jaehnig on 11/4/22.
//

import SwiftUI

struct NewNoteView: View {
    
    @ObservedObject var user_state = UserState.shared

    @State var note_title: String = "Note title...";
    @State var note_edited: String = "created just now";
    @State var note_content: String = "start writing...";
    @State var note_details_showing: Bool = false;

    var body: some View {
        VStack {
            VStack{
                HStack {
                    BackButton(note_title: $note_title, note_content: $note_content, close_action: "create")
                    Spacer()
                }
                NoteEditor(note_title: $note_title, note_content: $note_content)
                Spacer()
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
            VStack{
                HStack {
                    BackButton(note_title: $note_title, note_content: $note_content, close_action: "save")
                    Spacer()
                    DeleteNoteButton(note_details_showing: $note_details_showing)
                }
                if let note = user_state.notes[user_state.note_idx] {
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
    @Binding var note_title: String;
    @State var note_edited: String = "timestamp";
    @Binding var note_content: String;
    
    var body: some View {
        VStack {
            TextEditor(text: $note_title)
                .font(Font.custom("Inter-SemiBold", size: 25))
                .lineLimit(1)
                .frame(height: 40)
            HStack {
                Text(note_edited)
                    .font(Font.custom("Inter-Regular", size: 15))
                Spacer()
            }
            .padding([.leading], 3)
            .padding([.bottom], 25)
            TextEditor(text: $note_content)
                .font(Font.custom("Inter-Regular", size: 15))
        }
        .frame(width: 300)
    }
}

struct BackButton: View {
    @Binding var note_title: String;
    @Binding var note_content: String;
    @ObservedObject var user_state = UserState.shared
    var close_action: String;

    var body: some View {
        HStack {
            Button(action: {
                user_state.view = user_state.previous_view
                if(close_action == "save") { user_state.saveNote(user_state.notes[user_state.note_idx], note_title, note_content)}
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


struct DeleteNoteButton: View {
    @ObservedObject var user_state = UserState.shared
    @Binding var note_details_showing: Bool;
    
    var body: some View {
        Button(action: {
            user_state.deleteNote()
            note_details_showing = false
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
        HStack {
            ForEach(user_state.notes[user_state.note_idx].tags!, id: \.self) {tag in
                Tag(tag_content: tag!)
            }
        }
        .padding(.bottom, 10)
    }
}

struct Tag: View {
    var tag_content: String;
    
    var body: some View {
        Text(tag_content)
            .font(Font.custom("Inter-Regular", size: 15))
            .foregroundColor(.black)
            .padding([.top, .bottom], 5)
            .padding([.leading, .trailing], 15)
            .background(Color("grey"), in: RoundedRectangle(cornerRadius: 10))
    }
}

