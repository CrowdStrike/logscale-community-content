```
#event_simpleName=HttpRequestDetect
| parseHexString("HttpPostBody", as=b64data)
| format("%,.4s", field=b64data, as=b64data)
| MagicNumber := base64Decode(b64data, charset="UTF-8")
| MagicNumber=/^BZ(?<Version>\w{1})/i
| Version match {
	h => Version := "BZip2" ;
	H => Version := "BZip2 - Huffman" ;
	0 => Version := "BZip1" ;
}
| $HttpMethod()
| ImageFileName=/^\\HarddiskVolume\d(?<FilePath>.*\\)(?<FileName>.+)$/i
| format(format="C:%s", as=FilePath, field=[FilePath])
| HttpRequestHeader:=urlDecode(HttpRequestHeader)
| HttpRequestHeader=/User-Agent\:\s(?<UserAgentString>.+)\\u000d\\u000aHost/
| $AddComputerName()
| select([ComputerName, FileName, FilePath, HttpUrl, HttpMethod, MagicNumber, Version, UserAgentString, HttpRequestHeader])

```