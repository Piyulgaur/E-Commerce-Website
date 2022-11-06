//function for form validation
function validatePrice()
{
  //validation for name 
  var fn=document.getElementById("product_name").value;
  var reg1=/[a-zA-Z" "]{5,50}$/g;
  if(!reg1.test(fn))
  {
    alert(" Name must contain alphabet and length should be 5 to 20 character");
    return false;
  }
  
  if(fn.length<5 || fn.length>50)
  {
    alert(" Name must be having  5 to 50 character");
    return false;
  }
  

  //validation for Age
  var pin=document.getElementById("price").value;
  var regAge=/^[0-9]+$/;
  if(pin.length<=1 || pin.length>=5  )
  {
    alert("  price  should be atleast 1 to 99999 ");
    return false;
  }
  
  if(!regAge.test(pin))
  {
    alert("  Price  should contain only digit ");
    return false;
  }
  
  //validation for phone
  var pn=document.getElementById("instock").value;
  var reg2=/^[0-9]+$/;
  if(!reg2.test(pn))
  {
    alert("  instock must be of  digit ");
    return false;
  }
  
  

  
  var add=document.getElementById("desc").value;
  
  
  if(add.length<15 || add.length>500)
  {
    alert(" Address must be having  15 to 500 character");
    return false;
  }
  
}