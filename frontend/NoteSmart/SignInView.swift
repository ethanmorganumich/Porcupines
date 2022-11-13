//
//  signUpView.swift
//  NoteSmart
//
//  Created by Sam Jaehnig on 10/31/22.
//

import SwiftUI

struct SignInView: View {
    
    @State var username = ""
    @State var password = ""
    
    var body: some View {
        VStack {
            Text("sign-in")
                .font(Font.custom("Inter-SemiBold", size: 25))
            VStack {
                VStack {
                    FormTextField(result: $username, text_type: "", text: "username")
                    FormTextField(result: $password, text_type: "secure", text: "password")
                }
                .padding(.bottom, 20)
                StyledButton(next_view: "home view", text: "submit", color: "blue50")
                
            }
            .padding([.leading, .trailing], 75)
            .padding(.top, 100)
            .padding(.bottom, 75)
            TextButton(next_view: "sign-in view", text: "create an account?")
            TextButton(next_view: "forgot password view", text: "forgot your password?")
        }
    }
}
