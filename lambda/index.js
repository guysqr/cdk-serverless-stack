const AWSXRay = require('aws-xray-sdk-core')
const AWS = require('aws-sdk')
// Create client outside of handler to reuse
const lambda = new AWS.Lambda()

// Handler
exports.handler = async function (event, context) {
  console.log('## ENVIRONMENT VARIABLES: ' + serialize(process.env))
  console.log('## CONTEXT: ' + serialize(context))
  console.log('## EVENT: ' + serialize(event))
  try {
    return formatResponse("Hi there")
  } catch (error) {
    return formatError(error)
  }
}

var formatResponse = function (body) {
  var response = {
    "statusCode": 200,
    "headers": {
      "Content-Type": "text/html"
    },
    "isBase64Encoded": false,
    "multiValueHeaders": {
      "X-Custom-Header": ["My value", "My other value"],
    },
    "body": body
  }
  return response
}

var formatError = function (error) {
  var response = {
    "statusCode": error.statusCode,
    "headers": {
      "Content-Type": "text/plain",
      "x-amzn-ErrorType": error.code
    },
    "isBase64Encoded": false,
    "body": error.code + ": " + error.message
  }
  return response
}

var serialize = function (object) {
  return JSON.stringify(object, null, 2)
}