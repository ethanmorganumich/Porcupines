//
//  HomeView.swift
//  NoteSmart
//
//  Created by Sam Jaehnig on 10/30/22.
//

import SwiftUI

struct ViewManager: View {
    
    @ObservedObject var user_state = UserState.shared

    var body: some View {
        switch user_state.view {
        case "sign-up view":
            SignUpView()
        case "sign-in view":
            SignInView()
        case "home view":
            HomeView()
        case "new note view":
            NewNoteView()
        case "preview note view":
            PreviewNoteView()
        case "existing note view":
            ExistingNoteView()
        default:
            SetUpView()
        }
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ViewManager()
    }
}
