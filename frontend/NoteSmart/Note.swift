struct Note {
    var title: String?
    var text: String?
    var timestamp: String?
    var idx: Int?
    var id: String?
    var tags: [String?]?
    
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
