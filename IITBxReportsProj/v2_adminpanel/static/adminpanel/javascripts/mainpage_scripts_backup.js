<script>
function StartFetch3() 
{
//
//alert("call type 102")
    //////////alert('Start Fetch3 Ok')

    var startdate="2015-01-01"
    var enddate="2015-05-05"
//////////alert('Start Fetch3 Ok2')
    //document.write(enddate);
    var xmlhttp3;    
    if (window.XMLHttpRequest)
    {// code for IE7+, Firefox, Chrome, Opera, Safari
        xmlhttp3=new XMLHttpRequest();
    }
    else
    {// code for IE6, IE5
    xmlhttp3=new ActiveXObject("Microsoft.XMLHTTP");
    }
    xmlhttp3.onreadystatechange=function()
    {
    if (xmlhttp3.readyState==4 && xmlhttp3.status==200)
    {
        ////////alert("3got new data")
        //document.write("got new data");
		var obj = JSON.parse(xmlhttp3.responseText);
        var data = new Array();
var i =0;
for (var key in obj) 
{
    if(key != "DC")
    {
    data[i] = Number(obj[key]);
    //document.write(i+" "+data[i] +"<br>");
    i++;
    }
}
var name12 = new Array();
var name123 = new Array();
i=0;

for (var key in obj) 
{
    if(key != "DC")
    {
        name12[i]=key
    name123[i]=new Array()
    name123[i][0] = Date.parse(key)
    name123[i][1] = data[i]    
       // document.write(i+"nm12-> "+name12[i] +"<br>");
    i++;
    }
}
 var zipped = [],
    k;

for(k=0; k<data.length; ++k) {
    zipped.push({
        array1elem: name12[k],
        array2elem: data[k]
    });
}

zipped.sort(function(left, right) {
    var leftArray1elem = left.array2elem,
        rightArray1elem = right.array2elem;

    return leftArray1elem === rightArray1elem ? 0 : (leftArray1elem > rightArray1elem ? -1 : 1);
});

var array1 = [];
var array2 = [];
for(i=0; i<zipped.length; ++i) {
    array1.push(zipped[i].array1elem);
    array2.push(zipped[i].array2elem);
}
//////////alert("about to draw3")
EmailusagechartOptions.chart.width=(300+Math.round((1400/34)*array2.length))
EmailusagechartOptions.xAxis.categories=array1
EmailusagechartOptions.series[0].data=array2
//////////alert("3dataset")
var Emailchart = new Highcharts.Chart(EmailusagechartOptions);
//////////alert("3drawn")
//for(t=0;t<nj.length;t++)
//{
//document.write("<br>->"+nj[t].name+" "+nj[t].data+"<br>");
//}
//document.write(Math.round((800/34)*data.length));

        $(this).attr('disabled', false);
        }
  }
var URL = [location.protocol, '//', location.host, location.pathname].join('');
xmlhttp3.open("GET",URL+"?type=102&sd="+encodeURIComponent(startdate)+"&ed="+encodeURIComponent(enddate),true);
xmlhttp3.send(); 
        $(this).attr('disabled', false);

}    
//-----endajax
</script>
<!---------------------------------------------------------------------------------------------------------Start Fetch Function3 End ---- -->

<!-- -------------------------------------------------------------------------------------------------------start Fetch Function 2start -->
<script>
function StartFetch2() 
{
//alert("call type 101")
//StartFetch3()
    //////////alert('Start Fetch2 Ok')

    var startdate="2015-01-01"
    var enddate="2015-05-05"
//////////alert('Start Fetch2 Ok2')
    //document.write(enddate);
    var xmlhttp2;    
    if (window.XMLHttpRequest)
    {// code for IE7+, Firefox, Chrome, Opera, Safari
        xmlhttp2=new XMLHttpRequest();
    }
    else
    {// code for IE6, IE5
    xmlhttp2=new ActiveXObject("Microsoft.XMLHTTP");
    }
    xmlhttp2.onreadystatechange=function()
    {
    if (xmlhttp2.readyState==4 && xmlhttp2.status==200)
    {
        //alert("disku got new data")
        //document.write("got new data");
		var obj = JSON.parse(xmlhttp2.responseText);
        var data = new Array();
var i =0;
for (var key in obj) 
{
    if(key != "DC")
    {
    data[i] = Number(obj[key]);
    //document.write(i+" "+data[i] +"<br>");
    i++;
    }
}
var name12 = new Array();
var name123 = new Array();
i=0;

for (var key in obj) 
{
    if(key != "DC")
    {
        name12[i]=key
    name123[i]=new Array()
    name123[i][0] = Date.parse(key)
    name123[i][1] = data[i]    
       // document.write(i+"nm12-> "+name12[i] +"<br>");
    i++;
    }
}
 var zipped = [],
    k;

for(k=0; k<data.length; ++k) {
    zipped.push({
        array1elem: name12[k],
        array2elem: data[k]
    });
}

zipped.sort(function(left, right) {
    var leftArray1elem = left.array2elem,
        rightArray1elem = right.array2elem;

    return leftArray1elem === rightArray1elem ? 0 : (leftArray1elem > rightArray1elem ? -1 : 1);
});

var array1 = [];
var array2 = [];
for(i=0; i<zipped.length; ++i) {
    array1.push(zipped[i].array1elem);
    array2.push(zipped[i].array2elem);
}
//////////alert("about to draw")
DiskusagechartOptions.xAxis.categories=array1
DiskusagechartOptions.series[0].data=array2
//////////alert("dataset")
var Diskchart = new Highcharts.Chart(DiskusagechartOptions);
//////////alert("drawn2")

//for(t=0;t<nj.length;t++)
//{
//document.write("<br>->"+nj[t].name+" "+nj[t].data+"<br>");
//}
//document.write(Math.round((800/34)*data.length));

        $(this).attr('disabled', false);
        }
  }
var URL = [location.protocol, '//', location.host, location.pathname].join('');
xmlhttp2.open("GET",URL+"?type=101&sd="+encodeURIComponent(startdate)+"&ed="+encodeURIComponent(enddate),true);
xmlhttp2.send(); 
        $(this).attr('disabled', false);

}    
//-----endajax
</script>
<!---------------------------------------------------------------------------------------------------------Start Fetch Function2 End ---- -->


<!-- -------------------------------------------------------------------------------------------------------start Fetch Function start -->
<script>
function StartFetch() 
{
//alert("call type 100")
//StartFetch2()
    //////////alert('Start Fetch Ok')

    var startdate="2015-01-01"
    var enddate="2015-05-05"
    //document.write(enddate);
    var xmlhttp;    
    if (window.XMLHttpRequest)
    {// code for IE7+, Firefox, Chrome, Opera, Safari
        xmlhttp=new XMLHttpRequest();
    }
    else
    {// code for IE6, IE5
    xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
    }
    xmlhttp.onreadystatechange=function()
    {
    if (xmlhttp.readyState==4 && xmlhttp.status==200)
    {
        ////alert("got new data")
        //document.write("got new data");
        var obj2 = JSON.parse(xmlhttp.responseText);
        //document.write("got new data ok");
        var data2 = new Array();
        var i2 =0;
    for (var key2 in obj2) 
    {
    //document.write("hi");
    if(key2 != "course_id")
    {
    data2[i2] = Number(obj2[key2]);
    //document.write("data-> "+data2[i2] +"<br>");
    i2++;
    }
    }
//////////alert("parsed")
var name122 = new Array();
i2=0;
for (var key2 in obj2) 
{
    if(key2 != "course_id")
    {
    name122[i2] = key2;
    //document.write("name"+name122[i2] +"<br>");
    i2++;
    }
}
//////////alert("parsed2")
var name1234 = new Array();
itr=0;

for (var key in obj2) 
{
    if(key != "DC")
    {
    name1234[itr]=new Array()
    name1234[itr][0] = Date.parse(key)
    name1234[itr][1] = data2[itr]    
       //document.write(i+"nm12-> "+name1234[itr] +"<br>");
    itr++;
    }
}

LinechartOptions.series[0].data=name1234
var Linechart = new Highcharts.Chart(LinechartOptions);
//////////alert("drawv1")
//////////alert("drawn")
//for(t=0;t<nj.length;t++)
//{
//document.write("<br>->"+nj[t].name+" "+nj[t].data+"<br>");
//}
//document.write(Math.round((800/34)*data.length));

        $(this).attr('disabled', false);
        }
  }
var URL = [location.protocol, '//', location.host, location.pathname].join('');
xmlhttp.open("GET",URL+"?type=100&sd="+encodeURIComponent(startdate)+"&ed="+encodeURIComponent(enddate),true);
xmlhttp.send(); 
        $(this).attr('disabled', false);

}    
//-----endajax
</script>
<!---------------------------------------------------------------------------------------------------------Start Fetch Function End ---- -->
<!-- ----------------------------------------------------------------------------------------Main Data Read Section Start---- -->
<script type="text/javascript">
alert("call type 0")
var obj = {{ jsonobj|safe }};
var data = new Array();
var i =0;
for (var key in obj) 
{
    if(key != "DC")
    {
    data[i] = Number(obj[key]);
    //document.write(i+" "+data[i] +"<br>");
    i++;
    }
}
var name12 = new Array();
var name123 = new Array();
i=0;

for (var key in obj) 
{
    if(key != "DC")
    {
        name12[i]=key
    name123[i]=new Array()
    name123[i][0] = Date.parse(key)
    name123[i][1] = data[i]    
        //document.write(i+"nm12-> "+name12[i] +"<br>");
    i++;
    }
}
 var zipped = [],
    k;

for(k=0; k<data.length; ++k) {
    zipped.push({
        array1elem: name12[k],
        array2elem: data[k]
    });
}

zipped.sort(function(left, right) {
    var leftArray1elem = left.array2elem,
        rightArray1elem = right.array2elem;

    return leftArray1elem === rightArray1elem ? 0 : (leftArray1elem > rightArray1elem ? -1 : 1);
});

var array1 = [];
var array2 = [];
for(i=0; i<zipped.length; ++i) {
    array1.push(zipped[i].array1elem);
    array2.push(zipped[i].array2elem);
}
var dataArrayFinal = new Array()
var nj = [];
var nj2 = [];
for(j=0;j<name12.length;j++)
{ 
   nj.push({name: array1[j], data: array2[j]});
   nj2.push({name: name12[j], data: [data[j]]});
   var temp = new Array(name12[j],data[j]); 
   dataArrayFinal[j] = temp; 
   //document.write(dataArrayFinal[j]+"<br>");   
}
//document.write(data);
//for(t=0;t<nj.length;t++)
//{
//document.write("<br>->"+nj[t].name+" "+nj[t].data+"<br>");
//}
//document.write(Math.round((800/34)*data.length));
//////////alert("About to call")
StartFetch()
StartFetch2()
StartFetch3()
//alert("call type 0 ended")
</script>

<!-- --------------------------------------------------------------------------Main Data Read Section End ----------------------------- -->

<!-- -------------------------------------------------------------------------------Chart OPtions Section Start---------------------- -->
<script>
var EmailusagechartOptions = {
        chart: {
        renderTo: 'email_count',
            type: 'column',
						backgroundColor: "#232123"
            
        },
    
        title: {
            text: 'Coursewise Emails Sent',
        align: 'left',
        x:70,
		style: { color: 'white'}
        },
        xAxis: {
            categories: array1,
           
            tickInterval: 0,
			labels: {
				style: {
                    color: 'white'
                }
            }
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Number of emails',
				style: { color: 'white'},
                align: 'middle'
            },
            labels: {
                overflow: 'justify',
				style: { color: 'white'}
            }
        },
        tooltip: {
            valueSuffix: ''
        },
        plotOptions: {
            bar: {
                dataLabels: {
                    enabled: true
                }
            }
        },
        
        credits: {
            enabled: false
        },
        series: [{
		showInLegend: false,
        color: '#FFD68F',
            name: 'number of emails',
            data: array2
        }]
};
var DiskusagechartOptions = {
        chart: {
        renderTo: 'disk_usage',
            type: 'bar',
            height: (400+Math.round((1000/34)*data.length)),
			zoomType: 'y',
						backgroundColor: "#232123"
        },
        title: {
            text: 'Coursewise Disk Usage',
			style: { color: 'white'}
        },
        xAxis: {
            categories: array1,
            tickInterval: 0,
			labels: {
                overflow: 'justify',
				style: { color: 'white'}
            }
        },
        yAxis: {
			opposite:true,
            title: {
                text: null,
                align: 'middle'
            },
            labels: {
                overflow: 'justify',
				style: { color: 'white'}
            }
        },
        tooltip: {
            valueSuffix: 'Bytes',
			pointFormat: '{point.y}'
        },
        plotOptions: {
            bar: {
                dataLabels: {
                    enabled: false
                }
            }
        },
       
        credits: {
            enabled: false
        },
        series: [{
		showInLegend: false,
        color: '#00aaff',
            name: 'Student Strength',
            data: array2
        }]
};


var BarchartOptions = {
        chart: {
        renderTo: 'course_details',
            type: 'bar',
						backgroundColor: "#232123",
            height: (300+Math.round((800/34)*data.length))
        },
        title: {
            text: 'Coursewise Student Strength',
			style: { color: 'white'}
        },
        xAxis: {
            categories: array1,
            tickInterval: 0,
			labels: {

				style: {
                    color: 'white'
                }
            }
			
        },
        yAxis: {
		opposite:true,
            min: 0,
            title: {
                text: null,
                align: 'middle'
            },
            labels: {
                overflow: 'justify',
				style: {
                    color: 'white'
                }
            }
			 
        },
        tooltip: {
            valueSuffix: ''
        },
        plotOptions: {
            bar: {
                dataLabels: {
                    enabled: true
                }
            }
        },
        credits: {
            enabled: false
        },
        series: [{
		showInLegend: false,
        color: '#FFFFFF',
           name: 'Student Strength',
            data: array2
        }]
};
//alert("barchart options read")
var LinechartOptions = {
        chart: {
            renderTo: 'register_count',
            zoomType: 'xy',
			backgroundColor: "#232123"
        },
        title: {
            text: 'Students Registrations per Day',
			style: { color: 'white'}
        },
       
        xAxis: {
            type: 'datetime',
            dateTimeLabelFormats: { // don't display the dummy year
                month: '%e. %b',
                year: '%b'
            },
            title: {
                text: null,
				style: { color: 'white'}
            },
			labels: {
				style: {
                    color: 'white'
                }
            }
        },
        yAxis: {
            title: {
                text: 'No of Students Registered',
				style: { color: 'white'}
            },
            min: 0,
			labels: {
				style: {
                    color: 'white'
                }
            }
        },
        tooltip: {
            headerFormat: 'Date:',
            pointFormat: '{point.x:%e %b %Y} <br> Registrations:{point.y}'
        },

        plotOptions: {
            spline: {
                marker: {
                    enabled: true
                }
            }
        },

        series: [{
			showInLegend: false,
            color: '#ff8400',
            name: 'Student registrations',
            // Define the data points. All series have a dummy year
            // of 1970/71 in order to be compared on the same x axis. Note
            // that in JavaScript, months start at 0 for January, 1 for February etc.
            data: name123
        } ]
    };

////alert("optons read")
</script>

<!--- --------------------------------------------------------------------------------------------------------Chart OPtions Section End  -->
<script>

//for(t=0;t<datax.length;t++)
//{
//document.write("<br>->"+datax[t].name+" "+datax[t].data+"<br>");
//}
// Highcharts requires the y option to be set
$.each(nj, function (i, point) {
    point.y = point.data;
});

function getQueryParams(qs) {
    qs = qs.split('+').join(' ');

    var params = {},
        tokens,
        re = /[?&]?([^=]+)=([^&]*)/g;

    while (tokens = re.exec(qs)) {
        params[decodeURIComponent(tokens[1])] = decodeURIComponent(tokens[2]);
    }

    return params;
}

var query = getQueryParams(document.location.search);
var numparam = Number(query.type);

//if(numparam == 1)

//////////alert("BAR GRAPH");
//$(function () {
    //$('#container').highcharts({
BarchartOptions.series[0].data=array2  
 
var Barchart = new Highcharts.Chart(BarchartOptions);
//alert("about to plot barchart") 


</script>
<!--------------------------------------------------------------------------------------AJAX Function for updating Line graph Data --- -->
<script>
function ajaxfunc() 
{
   var startdate="2015-01-01"
    var enddate="2015-05-05"
    //document.write(enddate);
    var xmlhttp;    
    if (window.XMLHttpRequest)
    {// code for IE7+, Firefox, Chrome, Opera, Safari
        xmlhttp=new XMLHttpRequest();
    }
    else
    {// code for IE6, IE5
    xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
    }
    xmlhttp.onreadystatechange=function()
    {
    if (xmlhttp.readyState==4 && xmlhttp.status==200)
    {
        //////////alert("got new data")
        //document.write("got new data");
        var obj2 = JSON.parse(xmlhttp.responseText);
        //document.write("got new data ok");
        var data2 = new Array();
        var i2 =0;
    for (var key2 in obj2) 
    {
    //document.write("hi");
    if(key2 != "course_id")
    {
    data2[i2] = Number(obj2[key2]);
    //document.write("data-> "+data2[i2] +"<br>");
    i2++;
    }
    }
//////////alert("parsed")
var name122 = new Array();
i2=0;
for (var key2 in obj2) 
{
    if(key2 != "course_id")
    {
    name122[i2] = key2;
    //document.write("name"+name122[i2] +"<br>");
    i2++;
    }
}
//////////alert("parsed2")
var name1234 = new Array();
itr=0;

for (var key in obj2) 
{
    if(key != "DC")
    {
    name1234[itr]=new Array()
    name1234[itr][0] = Date.parse(key)
    name1234[itr][1] = data2[itr]    
       //document.write(i+"nm12-> "+name1234[itr] +"<br>");
    itr++;
    }
}
//document.write("name ok");
LinechartOptions.xAxis.min=Date.parse(startdate);
LinechartOptions.xAxis.max=Date.parse(enddate);
var chartnew = new Highcharts.Chart(LinechartOptions);
//////////alert("drawn")
//for(t=0;t<nj.length;t++)
//{
//document.write("<br>->"+nj[t].name+" "+nj[t].data+"<br>");
//}
//document.write(Math.round((800/34)*data.length));

        $(this).attr('disabled', false);
        }
  }
var URL = [location.protocol, '//', location.host, location.pathname].join('');
xmlhttp.open("GET",URL+"?type=103&sd="+encodeURIComponent(startdate)+"&ed="+encodeURIComponent(enddate),true);
xmlhttp.send(); 
        $(this).attr('disabled', false);

}    
</script>
<script language="javascript">var STATIC_URL = "{{ STATIC_URL|escapejs }}";</script>
<script> 
function myJsFunc()
{
var loc = window.location.pathname;
var dir = loc.substring(0, loc.lastIndexOf('/'));
var imgpath=STATIC_URL+"chartsapp/images/image6.gif"
var img_src_html="<img src=\""+imgpath+"\" style=\"display: block; margin: 0 auto;\">"
//alert(img_src_html)
//document.getElementById("page-wrapper").innerHTML = img_src_html;
document.getElementById("page_loader").style.display="block"
	var xmlhttp;    
    if (window.XMLHttpRequest)
    {// code for IE7+, Firefox, Chrome, Opera, Safari
        xmlhttp=new XMLHttpRequest();
    }
    else
    {// code for IE6, IE5
    xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
    }
    xmlhttp.onreadystatechange=function()
    {
    if (xmlhttp.readyState==4 && xmlhttp.status==200)
    {
        //alert("got new data")
		document.getElementById("page_loader").style.display="none"
		document.getElementById("page-wrapper").innerHTML = xmlhttp.responseText;
    }
}

var URL = [location.protocol, '//', location.host, dir,"/coursestructure"].join('');
//alert(URL)
xmlhttp.open("GET",URL,true);
xmlhttp.send(); 
//alert("ajax")

}
</script>