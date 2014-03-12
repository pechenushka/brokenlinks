var Alert = {
    template_id: "alert_template",
    error: function(message) {
        this.render('error', message);
    },
    success: function(message) {
        this.render('success', message);
    },
    info: function(message) {
        this.render('info', message);
    },
    render: function(type, message) {
        $("#alert").html("");

        $("#" + this.template_id).tmpl({
            type: type,
            message: message
        }).appendTo("#alert");
    }
}