//
//  signInView.swift
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
                if(user_state.failed_sign_in) {
                    Text("invalid login - please try again")
                        .padding([.top, .bottom], 5)
                        .padding([.leading, .trailing], 10)
                        .font(Font.custom("Inter-Regular", size: 15))
                        .background(Color("red_lighter"), in: RoundedRectangle(cornerRadius: 10))
                        .frame(width: 250)
                        
                }
                VStack {
                    FormTextField(result: $email, text_type: "", text: "email")
                    FormTextField(result: $password, text_type: "secure", text: "password")
                }
                .padding(.bottom, 20)
                StyledButton(action: {
                    user_state.signIn(email, password)
                    overlay_showing = true
                    user_state.failed_sign_in = false
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
    @ObservedObject var user_state = UserState.shared
    @Binding var overlay_showing: Bool;

    var body: some View {
        VStack {
            if overlay_showing && !user_state.failed_sign_in {
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
