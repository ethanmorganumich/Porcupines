//
//  signUpView.swift
//  NoteSmart
//
//  Created by Sam Jaehnig on 10/31/22.
//

import SwiftUI

struct SignInView: View {
    @ObservedObject var user_state = UserState.shared

    @State var email = ""
    @State var password = ""
    @State var overlay_showing: Bool = false;

    var body: some View {
        VStack {
            Text("sign-in")
                .font(Font.custom("Inter-SemiBold", size: 25))
            VStack {
                VStack {
                    FormTextField(result: $email, text_type: "", text: "email")
                    FormTextField(result: $password, text_type: "secure", text: "password")
                }
                .padding(.bottom, 20)
                StyledButton(action: {
                    user_state.signIn(email, password)
                    overlay_showing = true
                }, text: "submit", color: "blue50")
                
            }
            .padding([.leading, .trailing], 75)
            .padding(.top, 25)
            .padding(.bottom, 75)
            TextButton(next_view: "sign-up view", text: "create an account?")
        }
        .overlay(SignInOverlay(overlay_showing: $overlay_showing))
    }
}


struct SignInOverlay: View {
    @Binding var overlay_showing: Bool;

    var body: some View {
        VStack {
            if overlay_showing {
                Text("You will be signed-in shortly!")
                    .font(Font.custom("Inter-Regular", size: 20))
                    .multilineTextAlignment(.center)
                    .frame(width: 300, height: 100)
                    .padding([.top, .bottom], 150)
                    .padding([.leading, .trailing], 25)
            }
            
        }
        .background(Color("grey"), in: RoundedRectangle(cornerRadius: 10))

    }
}
