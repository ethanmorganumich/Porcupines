//
//  HomeView.swift
//  NoteSmart
//
//  Created by Sam Jaehnig on 10/31/22.
//

//
import SwiftUI

struct SetUpView: View {
    @ObservedObject var user_state = UserState.shared
    
    var body: some View {
        VStack {
            Spacer()
            WelcomeText()
            StyledButton(action: {user_state.view = "sign-in view"}, text: "sign-in", color: "blue50")
            StyledButton(action: {user_state.view = "sign-up view"}, text: "sign-up", color: "blue30")
            Spacer()
            BottomControlButtons()
        }
    }
}

struct WelcomeText: View {
    var body: some View {
        Text("welcome to")
            .font(Font.custom("Inter-Regular", size: 30))
        Text("NoteSmart")
            .font(Font.custom("Inter-Regular", size: 50))
    }
}

struct StyledButton: View {
    @ObservedObject var user_state = UserState.shared

    var action: () -> Void
//    var next_view: String
    var text: String
    var color: String
    
    var body: some View {
        VStack {
            Button(action: {
                action()
            }) {
                Text(text)
                    .font(Font.custom("Inter-Regular", size: 18))
                    .foregroundColor(.black)
            }
            .padding([.top, .bottom], 5)
            .padding([.leading, .trailing], 25)
            .background(Color(color), in: Capsule())
        }
    }
}
