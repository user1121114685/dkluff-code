// ==UserScript==
// @name           DKgr
// @namespace      http://userscripts.org/dkluffy
// @include        https://solutions.microstrategy.com/Helpdesk/open_tickets.asp?user=2
// ==/UserScript==

function addGlobalStyle(css) {
	var head, style;
	head = document.getElementsByTagName('head')[0];
	if (!head) { return; }
	style = document.createElement('style');
	style.type = 'text/css';
	style.innerHTML = css;
	head.appendChild(style);
}
function hideRow(mytable,patt){
	for(i=0;i<mytable.length;i++){
		if (mytable[i].textContent.search(patt) >= 0){
		//document.getElementById('tblMyOpenHelpdeskRequests').deleteRow(mytable[i].rowIndex)
		//mytable[i].style.display="none"
		mytable[i].hidden=true;
		}
	}
}
function showAllRow(mytable){
	for(i=0;i<mytable.length;i++){
		mytable[i].hidden=false;
	}
}

function highlightRow(mytable,patt,color){
	for(i=0;i<mytable.length;i++){
		if (mytable[i].textContent.search(patt) >= 0){
		//document.getElementById('tblMyOpenHelpdeskRequests').deleteRow(mytable[i].rowIndex)
		//mytable[i].style.display="none"
		mytable[i].style.background=color;
		}
	}	
}

function addHrefLink(mytable){
	for(i=0;i<mytable.length;i++){
		var elmtk = document.createElement('a');
		elmtk.href=mytable[i].cells[0].getElementsByTagName('a')[0].href;
		elmtk.textContent=mytable[i].cells[3].textContent;
		
		mytable[i].cells[3].replaceChild(elmtk,mytable[i].cells[3].firstChild);
	}
}

addGlobalStyle('.tablecell2{font-size:8pt;}');

var tktrs=document.getElementsByClassName("tablecell2");

highlightRow(tktrs,/New Submission/i,'yellow');
highlightRow(tktrs,/In Progress/i,'white');
addHrefLink(tktrs);

var elmBtdiv = document.createElement('div');
elmBtdiv.className="controllbar";
elmBtdiv.innerHTML="<a id='btshow_all' href=\"javascript:void();\">[Show All]</a> | <a id='bthide_wr' href=\"javascript:void();\">[Hide Waiting/Resolved]</a>"
document.body.appendChild(elmBtdiv);
addGlobalStyle('.controllbar{position:absolute;right:10%;top:5%;}');

document.getElementById('bthide_wr').addEventListener('click',function(){hideRow(tktrs,/waiting|Resolved/i);},false);
document.getElementById('btshow_all').addEventListener('click',function(){showAllRow(tktrs);},false);

hideRow(tktrs,/waiting|Resolved/i);

