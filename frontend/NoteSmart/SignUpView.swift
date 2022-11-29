//
//  signUpView.swift
//  NoteSmart
//
//  Created by Sam Jaehnig on 10/31/22.
//

import SwiftUI

struct SignUpView: View {
    
    @State var firstname = ""
    @State var lastname = ""
    @State var username = ""
    @State var email = ""
    @State var password = ""
    @State var password_repeated = ""
    
    var body: some View {
        VStack {
            Text("sign-up")
                .font(Font.custom("Inter-SemiBold", size: 25))
            VStack {
                VStack {
                    HStack {
                        FormTextField(result: $firstname, text_type: "", text: "first name")
                        FormTextField(result: $lastname, text_type: "", text: "last name")
                    }
                    FormTextField(result: $username, text_type: "", text: "username")
                    FormTextField(result: $email, text_type: "", text: "email")
                    FormTextField(result: $password, text_type: "secure", text: "password")
                    FormTextField(result: $password_repeated, text_type: "secure", text: "password (again)")
                }
                .padding(.bottom, 20)
                BaseStyledButton(action: {
                    UserState.shared.createUser(username, password)
                }, text: "submit", color: "blue50")
            }
            .padding([.leading, .trailing], 75)
            .padding(.top, 100)
            .padding(.bottom, 75)
            TextButton(next_view: "sign-in view", text: "already have an account?")
            TextButton(next_view: "forgot password view", text: "forgot your password?")
        }
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
            SecureField("password (again)", text: $result)
                .padding([.top, .bottom], 10)
                .padding([.leading, .trailing], 10)
                .font(Font.custom("Inter-Regular", size: 14))
                .background(Color("grey"), in: RoundedRectangle(cornerRadius: 10))
        default:
            TextField(text, text: $result)
                .padding([.top, .bottom], 10)
                .padding([.leading, .trailing], 10)
                .font(Font.custom("Inter-Regular", size: 14))
                .background(Color("grey"), in: RoundedRectangle(cornerRadius: 10))
        }
    }
}
