const React = require("react")

// Adds a class name to the body element
exports.onRenderBody = ({setHtmlAttributes}) => {
    setHtmlAttributes({lang: "ja"})
}