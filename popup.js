let btn = document.createElement("button");
btn.innerHTML = "Secure Tab";
btn.style.width = "113px"
btn.addEventListener("click", function() {
    
    chrome.tabs.query(
        {active:true},
        tabs=>{
            chrome.storage.sync.get("block_id",function(result){
                const tab=tabs[0];
                var current_tab = tab.url;

                var xhttp = new XMLHttpRequest();
                xhttp.open("POST", "http://127.0.0.1:5000/blocked", true);
                xhttp.setRequestHeader('Content-Type', 'application/json');
                var tab_json = JSON.stringify({"block_id": result.block_id, "blocked_url": current_tab})
                var block_json = tab_json
                xhttp.send(block_json)
                
                xhttp.onreadystatechange = function() {
                    if (this.readyState == 4 && this.status == 200) {
                        chrome.storage.sync.get("blocked_urls",function(result){
                            var dict = result.blocked_urls
                            dict.push(tab)
                            console.log("Dict: " + dict.length)
                            chrome.storage.sync.set({"blocked_urls": dict})
                            chrome.storage.sync.get("blocked_urls",function(result){
                                console.log("Blocked: " + result.blocked_urls.length)
                            })
                            let confirmed = document.createElement("p");
                            confirmed.innerHTML = "This website has been added to your blocked list. It will take 1-2 minutes before the website is blocked. "
                            btn.replaceWith(confirmed);

                        })
                    }
                }
            });
        }
    )
});

chrome.storage.sync.get("block_id",function(result){
    if (typeof result.key == "undefined"){ 
        var xhr = new XMLHttpRequest();
        xhr.open('GET', 'http://127.0.0.1:5000/extension/login');
        xhr.send();
        xhr.onreadystatechange = function() {
            if (xhr.readyState == XMLHttpRequest.DONE) {
                var response_json = JSON.parse(xhr.responseText);
                if (response_json["registered"] == false) {
                    var url = response_json["url"]
                    chrome.tabs.create({ url: url });

                } else {
                    var dict = {"email": response_json["email"], "block_id": response_json["block_id"], "blocked_urls": response_json["blocked_urls"]}
                    chrome.storage.sync.set(dict)
                    document.body.appendChild(btn);
                }
            }
        }
    } else {
        document.body.appendChild(btn);
    }
});


/*
// Get reference to background page.
const bgPage = chrome.extension.getBackgroundPage();
// Sign in with popup, typically attached to a button click.
bgPage.signInWithPopup();
*/
