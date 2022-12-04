struct Tag {
    var text: String?
    var id: String?
    
    @propertyWrapper
    struct NotePropWrapper {
        private var _value: String?
        var wrappedValue: String? {
            get { _value }
            set {
                guard let newValue = newValue else {
                    _value = nil
                    return
                }
                _value = (newValue == "null" || newValue.isEmpty) ? nil : newValue
            }
        }
        
        init(wrappedValue: String?) {
            self.wrappedValue = wrappedValue
        }
    }
}
