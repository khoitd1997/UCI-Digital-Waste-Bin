var myIndex = 0;
carousel();
runProgram();
function sleep(ms) {
	  return new Promise(resolve => setTimeout(resolve, ms));
}

async function runProgram()
{
	var readFlag = 0;
	var result1; //prev value
	var result2; //new value
	var objDate = new Date();
	var sec1 = objDate.getSeconds();
	var sec2 = sec1;
	var objDate2;
	while(true)
	{	
		objDate2 = new Date();
		sec2 = objDate2.getMilliseconds();
		await sleep(500); //sleep for 100 ms
		readTextFile("file:///C:/Users/Abel/Desktop/UCI-Digital-Waste-Bin-master%20(3)/UCI-Digital-Waste-Bin-master/v.01/results.json")
		console.log(result2);
		if(result2 != result1)
		{
			console.log("IT is different");
			result1 = result2;
			loading.style.visibility = "visible" ;
			await sleep(8000);
			loading.style.visibility = "hidden" ;
			
		}
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
				if(readFlag == 0)
				{
					result1 = xmlDoc.getElementsByTagName("result")[0].childNodes[0].nodeValue;
					readFlag = 1;
				}
				else {result2 = xmlDoc.getElementsByTagName("result")[0].childNodes[0].nodeValue;}
				
                console.log(result2*5);
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

