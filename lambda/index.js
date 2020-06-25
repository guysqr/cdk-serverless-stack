var AWSXRay = require('aws-xray-sdk-core');
var htmlCreator = require('html-creator');

// Handler
exports.handler = async function (event, context) {
  // console.log('## ENVIRONMENT VARIABLES: ' + serialize(process.env));
  // console.log('## CONTEXT: ' + serialize(context));
  // console.log('## EVENT: ' + serialize(event));
  AWSXRay.captureFunc('annotations', function (subsegment) {
    subsegment.addAnnotation('Note', 'foo was here');
  });

  var html = new htmlCreator([
    {
      type: 'head',
      content: [{ type: 'title', content: context.functionName }],
    },
    {
      type: 'body',
      attributes: { style: 'margin: 100px; background: #009933; color: white; font-family: Arial, Helvetica, sans-serif' },
      content: [
        {
          type: 'div',
          content: [
            {
              type: 'h1',
              content: 'Stepfunctions Pipeline Demo',
            },
            {
              type: 'p',
              content: "This is the Lambda function called '" + context.functionName + "'",
              attributes: {},
            },
          ],
        },
      ],
    },
  ]);

  try {
    return formatResponse(html.renderHTML(), context);
  } catch (error) {
    return formatError(error);
  }
};

var formatResponse = function (body, context) {
  var response = {
    statusCode: 200,
    headers: {
      'Content-Type': 'text/html',
    },
    isBase64Encoded: false,
    multiValueHeaders: {
      'X-Lambda-Name': [context.functionName],
    },
    body: body,
  };
  return response;
};

var formatError = function (error) {
  var response = {
    statusCode: error.statusCode,
    headers: {
      'Content-Type': 'text/plain',
      'x-amzn-ErrorType': error.code,
    },
    isBase64Encoded: false,
    body: error.code + ': ' + error.message,
  };
  AWSXRay.captureFunc('annotations', function (subsegment) {
    subsegment.addAnnotation('Note', 'an error happened');
  });
  return response;
};

var serialize = function (object) {
  return JSON.stringify(object, null, 2);
};
