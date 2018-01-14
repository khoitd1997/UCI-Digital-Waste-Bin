		var myIndex = 0;
		carousel();

function carousel() {
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
