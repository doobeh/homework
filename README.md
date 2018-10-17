## Homework

This is a pretty bare-bones project that exists to allow development
of a paired client.  The project implements fairly common data-flows,
it is a consumer of client data, and stores that data within a 
SQLite3 database.

The purpose is to be able to spin up this service, and set a challenge
to a third-party to be able to create a client (in any language) 
that can successfully communicate and populate the service with data.

So, we're aiming to test:

- Authentication that returns a temporary token, which can then be
  used to authenticate future requests with a 10 minute lifetime.
- Handle POST'd json data to API endpoints.
- Image/Binary uploads to API endpoints.
- JSON responses to requests.
- Basic UI, because, why not-- enables simple checks.

And the general goal is to build a client that can talk with this
service, to supply it with the correct data.

The steps would generally be:

1. Request an authentication token
2. Upload an image, get reference
3. Upload meta-data with image reference

When sending a second image, the client should just start from step 2
and use the currently active token. If the token expires and the client
gets a 401 - bad_token, only then should the client request a new 
token and resubmit.


## Endpoints

### Authentication &amp; Tokenization

```/api/v1/auth```

accepts a BasicAuth user/password-- returns a json dict:

```json
{
    "status": "success",
    "token": "E1@-91283901273987",
    "message": "Login Successful"
}
 ```
 
 example curl request:
 
    curl --user email@example.com:secretpassword homework.example.com/api/v1/auth
 
 
 A bad authentication token or auth will return a http code 401.
 Tokens can't be requested for other tokens (401 error).
 
 The token can now be used in place of the user in a BasicAuth request
 (The password can be anything, as it's discarded)

 ### Image Uploads

Data is uploaded in two sets, first the image is uploaded, 
and a reference returned-- then the meta-data (description,
etc) can be uploaded with the matching reference to link 
them together: 
 
 ```/api/v1/image```
 
 Accepts a multipart/form-data `image` and returns a json dict
 reference, expects an active Authentication token.
 
 ```json
{
    "status": "success",
    "reference": 2,
    "message": "File Uploaded."
}
```

Failures on uploads cause a 400 status code, with following JSON payload:

```json
{
    "status": "upload_failed",
    "message": "Upload failed"

}
```

example curl command:

    curl --user current_token:none -F "image=@sea.jpg" homework.example.com/api/v1/image

### MetaData Submission

```/api/v1/meta```

Accepts a JSON dict of the following fields:

```json
{
    "description": "Image Description",
    "url": "https://www.google.com",
    "date": "2007-03-04T21:08:12",
    "reference": 2
}
```

- `date` is ISO8601 compatible, 
- `reference` is an integer stored from the upload process.

Bad reference on meta data uploads cause a http code 400 with following payload:

```json
{
    "status": "bad_reference",
    "message": "Image reference lookup failure"
}
```

Other bad meta-data error (http code 400) with payload:
```json
{
    "status": "meta_failure",
    "message": "Meta-data failed"
}
```

### Reading Entries

```/api/v1/entries```

Returns a list of JSON objects describing the entries, from newest to oldest,
to allow the client to render a UI of results.

```json
{
    "entries": [
       {
           "reference": 1,
           "image": "http://example.service/uploaded-image.jpg",
           "description": "Example Description",
           "date": "2017-03-04T10:10:10",
           "url": "https://www.google.com/"
       },
       {
           "reference": 2,
           "image": "http://example.service/next-image.jpg",
           "description": "Next Description",
           "date": "2018-03-04T12:12:12",
           "url": "https://www.bing.com/"
       }
    ]
}

```