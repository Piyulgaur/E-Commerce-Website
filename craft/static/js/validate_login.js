//function for form validation
function validate()
{
  //validation for name 
  var fn=document.getElementById("name").value;
  var reg1=/[a-zA-Z" "]{3,20}$/g;
  if(!reg1.test(fn))
  {
    alert(" Name must contain alphabet and length should be 3 to 20 character");
    return false;
  }
  
  if(fn.length<5 || fn.length>30)
  {
    alert(" Name must be having  5 to 30 character");
    return false;
  }
  

  //validation for pin
  var pin=document.getElementById("pincode").value;
  var regAge=/^[0-9]+$/;
  if(pin.length<=4 || pin.length>=8  )
  {
    alert("  PIN code  should be atleast 4 to 8 character long ");
    return false;
  }
  
  if(!regAge.test(pin))
  {
    alert("  PIN should contain only digit ");
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
  
  

  //validation for password
  var pass=document.getElementById("password").value;
  var passReg=/^[a-zA-Z0-9]+$/;
  // validation for password 
  if(!passReg.test(pass))
  {
    alert(" password must contain alphabet and digits only");
    return false;
  }

  if(pass.length<8 || pass.length>15)
  {
    alert(" Password must contain 8 to 15 character only");
    return false;
  }

  var add=document.getElementById("street_address").value;
  
  
  if(add.length<15 || fn.length>150)
  {
    alert(" Address must be having  15 to 150 character");
    return false;
  }
  
}