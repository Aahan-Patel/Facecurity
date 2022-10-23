/*const app = firebase.initializeApp(config);
const auth = app.auth();
const signInWithPopup = () => {
  const provider = new firebase.auth.GoogleAuthProvider();
  return auth.signInWithPopup(provider).catch((error) => {
    console.log(error);
  })
};*/

var blockedLinks = [];



chrome.storage.sync.get("blocked_urls",function(result){
    blockedLinks = result.blocked_urls
})
chrome.tabs.onUpdated.addListener(function (tabId, changeInfo, tab) { // listener for tab opens
    if (changeInfo.status == 'loading') {
       // when the page is loading (you can do info.status === 'complete' but you will see the page for a second or two)
        for (var i = 0; i<blockedLinks.length; i++){
            if (tab.url === blockedLinks[i]) {
                chrome.tabs.query({ // change the tab url
                    currentWindow: true,
                    active: true
                }, function (tab) {
                    chrome.storage.sync.get("block_id",function(result){
                        var index = blockedLinks.indexOf(tab[0].url)
                        chrome.tabs.update(tab.id, {
                            url: 'http://127.0.0.1:5000//cam/confirm/' + result.block_id + "?index=" + index
                        });
                        chrome.storage.sync.set({"blocked_urls": blockedLinks})


                    });
            });
            }
        }
    }
})
