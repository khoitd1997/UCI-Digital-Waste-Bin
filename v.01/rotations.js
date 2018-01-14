var myIndex = 0;
carousel();
runProgram();
function sleep(ms) {
	  return new Promise(resolve => setTimeout(resolve, ms));
}

async function runProgram()
{
	var objDate = new Date();
	var sec1 = objDate.getSeconds();
	var sec2 = sec1;
	var objDate2;
	while(true)
	{	
		objDate2 = new Date();
		sec2 = objDate2.getMilliseconds();
		await sleep(500); //sleep for 100 ms
		readTextFile("file:///home/masa/gitProjects/UCI-Digital-Waste-Bin/v.01/result.json")
		//console.log("asfeaesfa");
		//console.log(sec2-sec1);
		//if(sec2 - sec1 >= 400)
		//	{
		//	carousel(); 
		//	}
	}
}

function readTextFile(file)
{
    var rawFile = new XMLHttpRequest();
    rawFile.open("GET", file, false);
    rawFile.onreadystatechange = function ()
    {
        if(rawFile.readyState === 4)
        {
            if(rawFile.status === 200 || rawFile.status == 0)
            {
                var allText = rawFile.responseText;
                //alert(allText);
                parser = new DOMParser();
                xmlDoc = parser.parseFromString(allText,"text/xml");
                console.log(xmlDoc.getElementsByTagName("result")[0].childNodes[0].nodeValue);
            }
        }
    }
    rawFile.send(null);
}

async function carousel() {
	var i;
	var x = document.getElementsByClassName("mySlides");
	for (i = 0; i < x.length; i++) {
		x[i].style.display = "none";  
	}
	myIndex++;
	if (myIndex > x.length) {myIndex = 1}    
	x[myIndex-1].style.display = "block";  
	var d = new Date();
	var n = d.getSeconds();
	var n2 = n;

	setTimeout(carousel, 8000); // Change image every 2 seconds
}

    //var reader; //GLOBAL File Reader object for demo purpose only

    /**
     * Check for the various File API support.
     */

