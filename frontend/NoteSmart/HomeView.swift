//
//  signUpView.swift
//  NoteSmart
//
//  Created by Sam Jaehnig on 10/31/22.
//

import SwiftUI

struct HomeView: View {
    @ObservedObject var user_state = UserState.shared

    var body: some View {
        VStack {
            // profile
            ProfileButtonView()
            // search & filter icons
            SearchFilterIconsView()
            // list items
            NotePreviewsView()
            //bottom control buttons
            Spacer()
            BottomControlButtons()
        }
        .onAppear() {user_state.getNotes()}
    }
}

struct ProfileButtonView : View {
    var body : some View {
        HStack {
            Spacer()
            Button(action: {}) {
                Spacer()
                Text("SJ")
                    .font(Font.custom("Inter-Regular", size: 21))
                    .frame(width: 50, height: 50, alignment: .center)
                    .background(Color("blue50"), in: Circle())
                    .foregroundColor(.black)
            }
            .padding(.bottom, 50)
            .padding(.trailing, 25)
        }
    }
}

struct SearchFilterIconsView : View {
    var body: some View {
        HStack {
            Button(action: {}) {
                Image(systemName: "magnifyingglass")
                    .font(.system(size: 30))
                    .foregroundColor(Color("blue70"))
            }
//            Button(action: {}) {
//                Image(systemName: "slider.horizontal.3")
//                    .font(.system(size: 30))
//                    .foregroundColor(Color("blue70"))
//            }
            Spacer()
        }
        .frame(width: 300)
        .padding([.bottom], 10)
    }
}


struct NotePreviewsView: View {
    @ObservedObject var user_state = UserState.shared
    
    var body: some View {
        List(user_state.notes.indices, id: \.self) {
            NoteItemView(note: user_state.notes[$0], idx: $0)
                .listRowSeparator(.hidden)
                .listRowInsets(.init(top: 10, leading: 0, bottom: 10, trailing: 0))
        }
        .frame(width: 300)
        .listStyle(PlainListStyle())
        .refreshable {
            user_state.getNotes()
        }
    }
}

struct NoteItemView: View {
    var note: Note
    var idx: Int
    @ObservedObject var user_state = UserState.shared
    
    var body: some View {
        Button(action: {
            user_state.viewNote(idx)
        }) {
            VStack {
                HStack {
                    Text(note.title!)
                        .font(Font.custom("Inter-Regular", size: 18))
                    Spacer()
                    if note.tags!.count > 0 {
                        Text(note.tags![0]!)
                            .font(Font.custom("Inter-Regular", size: 15))
                            .foregroundColor(.black)
                            .padding([.top, .bottom], 5)
                            .padding([.leading, .trailing], 15)
                            .background(.white, in: RoundedRectangle(cornerRadius: 10))
                    }
                }
                .frame(height: 30)
                HStack {
                    Text(note.text!)//(note.timestamp! + " - " + note.text!)
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
