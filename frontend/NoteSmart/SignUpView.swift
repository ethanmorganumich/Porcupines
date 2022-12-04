//
//  signUpView.swift
//  NoteSmart
//
//  Created by Sam Jaehnig on 10/31/22.
//

import SwiftUI

struct SignUpView: View {
    @ObservedObject var user_state = UserState.shared

    @State var email = ""
    @State var password = ""
    @State var overlay_showing: Bool = false;
    
    var body: some View {
        VStack {
            Text("sign-up")
                .font(Font.custom("Inter-SemiBold", size: 25))
            VStack {
                VStack {
                    FormTextField(result: $email, text_type: "", text: "email")
                    FormTextField(result: $password, text_type: "secure", text: "password")
                }
                .padding(.bottom, 20)
                StyledButton(action: {
                    user_state.signUp(email, password)
                    overlay_showing = true
                }, text: "submit", color: "blue30")
            }
            .padding([.leading, .trailing], 75)
            .padding(.top, 25)
            .padding(.bottom, 75)
            TextButton(next_view: "sign-in view", text: "already have an account?")
        }
        .overlay(SignUpOverlay(overlay_showing: $overlay_showing, email: $email, password: $password))
    }
}



struct TextButton: View {
    
    var next_view: String;
    var text: String;
    
    var body: some View {
        Button(action: {
            UserState.shared.view = next_view
        }) {
            Text(text)
                .font(Font.custom("Inter-Regular", size: 15))
                .foregroundColor(.black)
                .italic()
                .underline()
        }
    }
}

struct FormTextField: View {
    @Binding var result: String;
    var text_type: String;
    var text: String;
    
    var body: some View {
        switch text_type {
        case "secure":
            SecureField("password", text: $result)
                .padding([.top, .bottom], 10)
                .padding([.leading, .trailing], 10)
                .font(Font.custom("Inter-Regular", size: 14))
                .background(Color("grey"), in: RoundedRectangle(cornerRadius: 10))
                .autocapitalization(.none)
        default:
            TextField(text, text: $result)
                .padding([.top, .bottom], 10)
                .padding([.leading, .trailing], 10)
                .font(Font.custom("Inter-Regular", size: 14))
                .background(Color("grey"), in: RoundedRectangle(cornerRadius: 10))
                .autocapitalization(.none)
        }
    }
}

struct SignUpOverlay: View {
    @ObservedObject var user_state = UserState.shared

    @Binding var overlay_showing: Bool;
    @Binding var email: String;
    @Binding var password: String;
    
    @State var show_submit: Bool = true;
    @State var signup_message: String = "Please check your email and click the link provided to finish signing-up! When you are done, click here:"
    
    var body: some View {
        if overlay_showing {
            VStack {
                Spacer()
                Text(signup_message)
                    .font(Font.custom("Inter-Regular", size: 20))
                    .multilineTextAlignment(.center)
                    .padding([.leading, .trailing], 25)
                if show_submit {
                    StyledButton(action: {
                        user_state.signIn(email, password)
                        show_submit = false
                        signup_message = "You will be signed-in shortly!"
                    }, text: "done", color: "blue30")
                    .padding([.top], 25)
                    Spacer()
                }
                Spacer()
            }
            .frame(minHeight: 300)
            .frame(width: 300)
            .background(Color("grey"), in: RoundedRectangle(cornerRadius: 10))
        }
    }
}
