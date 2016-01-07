

var ss = SpreadsheetApp.openById('## my spreadsheet key ##');
var ifttSheet = ss.getSheetByName('Sheet1');
var logSheet = ss.getSheetByName('Event Log');

function myFunction() {
  logSheet.clearContents();
  var data = ifttSheet.getDataRange().getValues();
  
  logSheet.appendRow(["Year","Month","Day","Hour","Duration","Activity"])
  for(i=0;i < data.length-1;i++){
    var rowA = data[i],
      eventDateA = parseIfttDate(rowA[0].toString()),
      eventA = rowA[2];
      
    var rowB = data[i+1],
      eventDateB = parseIfttDate(rowB[0].toString()),
      eventB = rowB[2]; 
        
    var msMinute = 60*1000;
    var msDay = 60*60*24*1000;
      
    var lapsedTime0 = Math.floor(((eventDateB - eventDateA) % msDay) / msMinute);
    var activity = determineActivity(eventA,eventB);
    var myMonth = eventDateA.getMonth()
    if (eventDateA.getMonth() == 0){myMonth=12}  //I couldn't get it to stop saying that december is a 0, so I just fixed it with this bandaid.
    logSheet.appendRow([eventDateA.getYear(),myMonth,eventDateA.getDate(),eventDateA.getHours(),lapsedTime0,activity])
    }
  }

function parseIfttDate(myStr){

  var mL = {'January':1, 'February':2, 'March':3, 'April':4, 'May':5, 'June':6, 'July':7, 'August':8,
            'September':9, 'October':10, 'November':11, 'December':12};            
  var myArray = myStr.replace(' at', "").split(" ");
  var myMonth = mL[myArray[0]];
  var myDate = myArray[1].replace(',','');
  var myYear = myArray[2];
  var myTime = myArray[3];
  var myHours = myTime.substring(0, 2);
  if (myTime.indexOf("PM")!=-1){
    if (myTime.substring(0, 1)=='0'){myHours = myTime.substring(1, 2);}
    if (myHours!="12"){myHours = String(parseInt(myHours) +  12)}
  }
  var myMinutes = myTime.substring(3, 5);
  if (myTime.substring(3, 4)=='0'){myMinutes = myTime.substring(4, 5);}  

  var d = new Date(myYear, myMonth, myDate,myHours,myMinutes,0,0)
  var returnValues = [myMonth,myDate,myYear,"\'"+myMinutes,"\'"+myTime,myHours,"\'"+String(d)]
  return d
  }

function determineActivity(A,B){
 var discovery = "unable to determine activity";
    //home and work functions:
    if((A  == "Leaving Work")&&(B == "Arriving at Home")){discovery = "Going from work to home"}
    if((A  == "Arriving at Home")&&(B == "Leaving Home")){discovery = "Hanging out at home"}
    if((A  == "Leaving Home")&&(B == "Arriving at Home")){discovery = "Went out, not to work"}
    if((A  == "Leaving Home")&&(B == "Arriving at Work")){discovery = "Going from home to work"}
    if((A  == "Arriving at Work")&&(B == "Leaving Work")){discovery = "Working"}
    if((A  == "Leaving Work")&&(B == "Arriving at Work")){discovery = "Left work for a bit, and came back"}
    //functions for my girlfried's place:
    if((A  == "Leaving Home")&&(B == "entered stacias house")){discovery = "Going from home to Stacia's"}
    if((A  == "left Stacias place")&&(B == "entered stacias house")){discovery = "Left Stacia's place for a bit, and came back"}
    if((A  == "entered stacias house")&&(B == "left Stacias place")){discovery = "Hanging out at Stacia's"}
    if((A  == "Leaving Work")&&(B == "entered stacias house")){discovery = "Going from work to Stacia's"}
    if((A  == "left Stacias place")&&(B == "Arriving at Work")){discovery = "Going from Stacia's to work"}
    if((A  == "left Stacias place")&&(B == "Arriving at Home")){discovery = "Going from Stacia's place to home"}
    //Handling odd duplicates and missing logs
    if((A  == "Leaving Work")&&(B == "Leaving Work")){discovery = "Working"}
    if((A  == "Leaving Home")&&(B == "Leaving Home")){discovery = "Hanging out at home"}
  return discovery;
 }