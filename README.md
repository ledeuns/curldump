## What is curldu.mp ?
curldu.mp is a free and open-source service to exchange small files with cURL.

**Never upload confidential files, they are not protected from eavesdropping**

## Usage :

* To upload a file :
  `curl -T /home/myfile curldu.mp`
or
  `curl -File=@/home/myfile curldu.mp`

* To upload multiple files :
  `curl -T {/home/myfile, file2} curldu.mp`
or
  `curl -File=@/home/myfile -File1=@myfile curldu.mp`

* To upload a stream :
 `curl http://curldu.mp | curl -T - curldu.mp`

* To protect access to your file with HTTP basic authentication :
  `curl -u user:password -T /home/myfile curldu.mp`
(better use HTTPS for safety)

curldu.mp returns a (list of) URLs. To get a shorter URL, send the *X-SHORT: yes* HTTP header :
  `curl -H "X-SHORT: yes" -T /home/myfile curldu.mp`
Shorter URLs are cleaned after 30 days.

To download, just `curl -o myfile http://curldu.mp/6722767993cc75af7d400df472c04d84ea0b6b7d` or paste the returned URL in your browser. Add the *?attach* parameter to download as an attachment.

## Dependencies
curldu.mp depends on :
* Flask
* uwsgi
* python-magic
* sqlite3

## Limitations
curldu.mp needs a webserver (Nginx/Apache) to handle Chunked Transfer Encoding (used when content is piped)

## Credits :
curldu.mp is an alternative to http://chunk.io under the free software ISC licence. You can freely install it on your own server. Fork me at https://github.com/ledeuns/curldump.
