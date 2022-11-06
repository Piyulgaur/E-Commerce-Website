//function for form validation
function validateAdmin()
{
  //validation for name 
  var fn=document.getElementById("name").value;
  var reg1=/[a-zA-Z" "]{5,20}$/g;
  if(!reg1.test(fn))
  {
    alert(" Name must contain alphabet and length should be 5 to 20 character");
    return false;
  }
  
  if(fn.length<5 || fn.length>30)
  {
    alert(" Name must be having  5 to 30 character");
    return false;
  }
  

  //validation for Age
  var pin=document.getElementById("gst").value;
  var regAge=/^[0-9]+$/;
  if(pin.length<=6 || pin.length>=12  )
  {
    alert("  GSTIN  should be atleast 6 to 12 character long ");
    return false;
  }
  
  if(!regAge.test(pin))
  {
    alert("  GSTIN NO.  should contain only digit ");
    return false;
  }
  
  //validation for phone
  var pn=document.getElementById("phone_number").value;
  var reg2=/^[0-9]{10}$/;
  if(!reg2.test(pn))
  {
    alert("  Phone number must be of 10 digit ");
    return false;
  }
  

  
  var add=document.getElementById("street_address").value;
  
  
  if(add.length<15 || add.length>150)
  {
    alert(" Address must be having  15 to 150 character");
    return false;
  }
  
}