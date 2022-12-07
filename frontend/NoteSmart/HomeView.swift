//
//  HomeView.swift
//  NoteSmart
//
//  Created by Sam Jaehnig on 10/31/22.
//

import SwiftUI

struct HomeView: View {
    @ObservedObject var user_state = UserState.shared

    var body: some View {
        VStack {
            ProfileIconView()
            NotePreviewsView()
            Spacer()
            BottomControlButtons()
        }
        .onAppear() {
            user_state.getNotes()
        }
    }
}

struct ProfileIconView : View {
    @ObservedObject var user_state = UserState.shared
    
    var body : some View {
        HStack {
            Spacer()
            Text(user_state.email[...user_state.email.index(user_state.email.startIndex, offsetBy: 1)])
                .font(Font.custom("Inter-Regular", size: 21))
                .frame(width: 50, height: 50, alignment: .center)
                .background(Color("blue50"), in: Circle())
                .foregroundColor(.black)
                .padding(.bottom, 10)
                .padding(.trailing, 25)
        }
    }
}

struct NotePreviewsView: View {
    @ObservedObject var user_state = UserState.shared
    @State var search: String = "";
    
    var body: some View {
        NavigationView {
            List(user_state.notes.indices, id: \.self) {
                if (search == "" || user_state.searchTagMatch(search, user_state.notes[$0].tags!)){
                    NoteItemView(note: user_state.notes[$0])
                        .listRowSeparator(.hidden)
                        .listRowInsets(.init(top: 10, leading: 0, bottom: 10, trailing: 0))
                }
            }
            .listStyle(PlainListStyle())
            .frame(width: 300)
        }
        .frame(width: 350, height: 600)
        .searchable(text: $search, prompt: "search tags here...")
        .font(Font.custom("Inter-Regular", size: 15))
        
        
        if(search != "") {
            HStack {
                if let tags = user_state.filterTagMatches(true, search, user_state.tags) {
                    ForEach(tags.indices, id: \.self) {
                        TagItem(tag: tags[$0])
                    }
                }
            }
            .padding(.bottom, 10)
            .padding([.leading, .trailing], 20)
        }
    }
}

struct NoteItemView: View {
    var note: Note
    @ObservedObject var user_state = UserState.shared
    
    var body: some View {
        Button(action: {
            user_state.viewNote(note.id!)
        }) {
            VStack {
                HStack {
                    Text(note.title!)
                        .font(Font.custom("Inter-Regular", size: 18))
                    Spacer()
                    if note.tags!.count > 0 {
                        Text(note.tags![0].text!)
                            .font(Font.custom("Inter-Regular", size: 15))
                            .foregroundColor(.black)
                            .padding([.top, .bottom], 5)
                            .padding([.leading, .trailing], 15)
                            .background(.white, in: RoundedRectangle(cornerRadius: 10))
                    }
                }
                .frame(height: 30)
                HStack {
                    Text(note.text!)
                        .font(Font.custom("Inter-Regular", size: 15))
                        .lineLimit(1)
                    Spacer()
                }
            }
            .padding([.leading, .trailing], 15)
            .padding([.top, .bottom], 15)
            .background(Color("grey"), in: RoundedRectangle(cornerRadius: 10))
            .foregroundColor(.black)
        }
    }
}
