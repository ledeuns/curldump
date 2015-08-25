# What is curldu.mp ?
curldu.mp is a free and open-source service to exchange small files with cURL.

**Never upload confidential files**

# Usage :

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

curldu.mp returns a (list of) URLs. To get a shorter URL, send the *X-SHORT: yes* HTTP header :
  `curl -H "X-SHORT: yes" -T /home/myfile curldu.mp`

To download, just `curl -o myfile http://curldu.mp/6722767993cc75af7d400df472c04d84ea0b6b7d` or paste the returned URL in your browser. Add the *?attach* parameter to download as an attachment.


# Credits :
curldu.mp is an alternative to http://chunk.io under the free software ISC licence. You can freely install it on your own server. Fork me at https://github.com/ledeuns/curldump.
