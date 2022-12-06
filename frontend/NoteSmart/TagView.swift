
import SwiftUI

struct TagView: View {
    
    @ObservedObject var user_state = UserState.shared

    var body: some View {
        VStack {
            ProfileIconView()
            HStack{
                Text(user_state.tag_viewed.text!)
                    .font(Font.custom("Inter-Regular", size: 30))
            }
            .padding([.bottom], 10)
            TagNotePreviewsView()
            Spacer()
            BottomControlButtons()
        }
        .onAppear() {
            user_state.getNotes()
        }
    }
}

struct TagNotePreviewsView: View {
    @ObservedObject var user_state = UserState.shared
    
    var body: some View {
        NavigationView {
            List(user_state.notes.indices, id: \.self) {
                if(user_state.searchTagMatch(user_state.tag_viewed.text!, user_state.notes[$0].tags!)) {
                    NoteItemView(note: user_state.notes[$0])
                        .listRowSeparator(.hidden)
                        .listRowInsets(.init(top: 10, leading: 0, bottom: 10, trailing: 0))
                }
            }
            .listStyle(PlainListStyle())
            .frame(width: 300)
        }
        .frame(width: 350, height: 600)
        .font(Font.custom("Inter-Regular", size: 15))
    }
}

