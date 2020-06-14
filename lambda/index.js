const AWSXRay = require('aws-xray-sdk-core')
const AWS = AWSXRay.captureAWS(require('aws-sdk'))

// Create client outside of handler to reuse
const lambda = new AWS.Lambda()

// Handler
exports.handler = async function (event, context) {
  console.log('## ENVIRONMENT VARIABLES: ' + serialize(process.env))
  console.log('## CONTEXT: ' + serialize(context))
  console.log('## EVENT: ' + serialize(event))
  AWSXRay.captureFunc('annotations', function (subsegment) {
    subsegment.addAnnotation('Name', 'lambda-func');
    subsegment.addAnnotation('UserID', 'guy');
  });
  try {
    return formatResponse("<html><h1>Hi there</h1><body>Here is my output</body></html>")
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