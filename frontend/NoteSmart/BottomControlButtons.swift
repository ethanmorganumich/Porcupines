//
//  HomeView.swift
//  NoteSmart
//
//  Created by Sam Jaehnig on 10/31/22.
//

//
import SwiftUI

struct BottomControlButtons: View {
    @State var folder_intensity: Float = 0.5;
    @State var home_intensity: Float = 0.5;
    @State var edit_intensity: Float = 0.5;
    
    var body: some View {
        HStack {
//            Spacer()
//            Button(action: {}) {
//                Image(systemName: "folder")
//                    .font(.system(size: 30))
//                    .foregroundColor(Color("blue70"))
//            }
//            Spacer()
//            Button(action: {}) {
//                Image(systemName: "house")
//                    .font(.system(size: 30))
//                    .foregroundColor(Color("blue70"))
//            }
            Spacer()
            Button(action: {
                UserState.shared.previous_view = UserState.shared.view
                UserState.shared.view = "new note view"
            }) {
                Image(systemName: "square.and.pencil")
                    .font(.system(size: 30))
                    .foregroundColor(Color("blue70"))
            }
            Spacer()
        }
        
    }
}
