//
//  HomeView.swift
//  NoteSmart
//
//  Created by Sam Jaehnig on 10/31/22.
//

//
import SwiftUI

struct BottomControlButtons: View {
    @ObservedObject var user_state = UserState.shared
        
    var body: some View {
        HStack {
            Spacer()
            if(user_state.view == "") {
                Button(action: {
                    user_state.previous_view = UserState.shared.view
                    user_state.view = "new note view"
                    user_state.trial_demo = true
                }) {
                    Image(systemName: "square.and.pencil")
                        .font(.system(size: 30))
                        .foregroundColor(Color("blue70"))
                }
            } else if(user_state.view == "home view") {
                Button(action: {
                    user_state.previous_view = UserState.shared.view
                    user_state.view = "new note view"
                }) {
                    Image(systemName: "square.and.pencil")
                        .font(.system(size: 30))
                        .foregroundColor(Color("blue70"))
                }
            } else if(user_state.view == "tag view") {
                Button(action: {
                    user_state.view = "home view"
                }) {
                    Image(systemName: "house.fill")
                        .font(.system(size: 30))
                        .foregroundColor(Color("blue70"))
                }
            }
            Spacer()
            
        }
        
    }
}
