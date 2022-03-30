$(document).ready(function () {
    // better tables: don't interfere with calendar tables (border-top)
    $("table").addClass("table table-striped table-condensed table-responsive");

    // vertical align callout captions with icons
    $(".bs-callout h4").wrapInner("<span style='vertical-align:middle'></span>");
    // add icons to callouts
    var glyphicons = {
        "bs-callout-book"    : "glyphicon-book",
        "bs-callout-check"   : "glyphicon-check",
        "bs-callout-class"   : "glyphicon-blackboard",
        "bs-callout-lab"     : "glyphicon-zoom-in",
        "bs-callout-partner" : "glyphicon-random",
        "bs-callout-code"    : "glyphicon-wrench",
        "bs-callout-comm"    : "glyphicon-phone-alt",
        "bs-callout-danger"  : "glyphicon-flash",
        "bs-callout-environment" : "glyphicon-globe",
        "bs-callout-exam"    : "glyphicon-pencil",
        "bs-callout-info"    : "glyphicon-info-sign",
        "bs-callout-user"    : "glyphicon-user",
        "bs-callout-primary" : "glyphicon-tasks",
        "bs-callout-success" : "glyphicon-question-sign",
        "bs-callout-warning" : "glyphicon-exclamation-sign",
        "bs-callout-late" : "glyphicon-time"
    };
    $.each(glyphicons, function(k, v) {
        $("<span/>")
        .addClass("glyphicon " + v)
        .prependTo($("." + k +" h4"))
        .attr("aria-hidden", "true")
        .css("padding-right", "5px")
        .css("vertical-align", "middle");
        ;
    });
});

$(document).ready(function () {
    // complete emails
    var appmail = function (_, s) {
        return s + ["@cornell", "edu"].join(".");
    };
    $("a.cornell-cs-mail").text(appmail);
    $("a.cornell-cs-mail").attr("href", function () { return "mailto:" + this.text; });
});
