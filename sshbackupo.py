{% extends 'theme/main_template.html' %}
{% block content %}
{% load static %}
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
<script>

  document.addEventListener("DOMContentLoaded", function(){
  document.getElementById('route').click();
  setInterval(function() {

    var request = new XMLHttpRequest();
    request.open('GET', '{% static '/data/data.json' %}');
    request.onload = function(){
      var data = JSON.parse(request.responseText);
      renderHTML(data);
    };
    request.send();


  }, 1000);
  });


    function renderHTML(data)
    {
        var tbody= document.getElementById('tablebody');
        var route = document.getElementById('vlanBody');
        var swtable=''
        var routetable="";
        var trunk="";
        var spanning="";

        var table="";
        var routerinfo=""
        data['interface'].forEach(int =>{

          table +='<tr><td><a href="#my_modal" data-toggle="modal" data-id="'+int.interface+'"class="open-AddBookDialog btn btn-primary">' + int.interface +'</a></td><td>'+int.ip_address+'</td><td>'+int.link_status+'</td><td>'+int.protocol_status+'</td></tr>';
          tbody.innerHTML = table;

        });

        data['vlan'].forEach(vlan =>{

          routetable +='<tr><td><a href="#vlan_modal" data-toggle="modal" data-id="'+vlan.vlan_id+'"class="open-AddVlanDialog btn btn-primary">' + vlan.vlan_id +'</a></td><td>'+vlan.name+'</td><td>'+
            vlan.interfaces+'</td></tr>';

        });
        data['switchport'].forEach(sw =>{

          routetable +='<tr><td><a href="#sw_modal" data-toggle="modal" data-id="'+sw.interface+'"class="open-AddSwDialog btn btn-primary">' + sw.interface +'</a></td><td>'+vlan.mode+'</td><td>'+sw.access_vlan+'</td><td>'+sw.native_vlan+'</td><td>'+
            sw.trunking_vlans+'</td></tr>';

        });
        spanning +='<h3>Spanning Tree</h3><span style="white-space: pre-line"><p>'+data['spanning']+'</span></p>'
        trunk +='<h3>Trunk Interfaces</h3><span style="white-space: pre-line"><p>'+data['trunk']+'</span></p>'

        route.innerHTML = routetable;
        document.getElementById('Paris').innerHTML = spanning
        document.getElementById('Tokyo').innerHTML = trunk

        data['version'].forEach(ver =>{

          routerinfo +='<p id="routerinfo"><b>Hostname:</b>'+ver.hostname +'&emsp;<b>Uptime:</b>'+ver.uptime+'&emsp;<b>Version:</b>'+ver.version+'</p>';
          document.getElementById('routerinfo').innerHTML = routerinfo;

        });

    }


   $(document).on("click", ".open-AddBookDialog", function () {
     var intid = $(this).data('id');
     $(".modal-body #intid").val( intid );

   });
   $(document).on("click", ".open-AddVlanDialog", function () {
     var vlan_id = $(this).data('id');
     $(".modal-vlan #vlan_id").val( vlan_id );

   });
   $(document).on("click", ".open-AddSwDialog", function () {
     var int_id = $(this).data('id');
     $(".modal-sw #int_id").val( int_id );

   });

   function openCity(evt, cityName)
   {
      var i, tabcontent, tablinks;
      tabcontent = document.getElementsByClassName("tabcontent");
      for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
      }
      tablinks = document.getElementsByClassName("tablinks");
      for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
      }
      document.getElementById(cityName).style.display = "block";
      evt.currentTarget.className += " active";
   }


</script>

<!-- Page Heading -->
<form id="int-form" action="/swconfChange/" method="post">
{% csrf_token %}

<div class="modal fade" id="my_modal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel"
  aria-hidden="true">
  <div class="modal-dialog" role="document">
    <div class="modal-content">
      <div class="modal-header text-center">
        <div id="form-messages"></div>
        <h4 class="modal-title w-100 font-weight-bold">Change config</h4>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
      <div class="modal-body">
      <input type="hidden" name="intid" id="intid" value="">
        <div class="md-form mb-5">
          <label data-error="wrong" data-success="right" for="form34">IP address</label>
          <input type="text" name="ip" class="form-control data-fv-ip___ipv4">

        </div>
        <div class="md-form mb-5">
          <label data-error="wrong" data-success="right" for="form29">Subnet mask</label>
          <input type="text" name="mask" class="form-control validate">
        </div>
        <div class="md-form mb-5">
          <label data-error="wrong" data-success="right" for="form29">Line status(shutdown/noshutdown)</label><br>
          <input type="radio" id="shutdown" name="ls" value="shutdown">
          <label>Shutdown</label><br>
          <input type="radio" id="noshutdown" name="ls" value="no shutdown">
          <label>No Shutdown</label>

        </div>
      </div>
      <div class="modal-footer d-flex justify-content-center">
        <button class="btn btn-primary" type ="submit" name="submit">Save</button>
      </div>
    </div>
  </div>
</div>
</form>







  <div class="modal fade" id="vlan_modal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel"
    aria-hidden="true">
    <div class="modal-dialog" role="document">
      <div class="modal-content">
        <div class="modal-header text-center">
          <div id="form-messages"></div>
          <h4 class="modal-title w-100 font-weight-bold">Change VLAN Config</h4>
          <button type="button" class="close" data-dismiss="modal" aria-label="Close">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        <form  method="get" action="/swconfChange/">
        {% csrf_token %}
        <div class="modal-vlan">
          <div class="md-form mb-5">

              <input type="hidden" class="form-control" name="vlan_id" id="vlan_id">
          </div>
          <div class="md-form mb-5">

              <input type="text" class="form-control" name="vlan_name" placeholder="VLAN Name">
          </div>
          <div class="md-form mb-5">
          <button type="submit" class="btn btn-primary" name="submit">Save Name</button>
          <button type="submit" class="btn btn-danger" name="remove">Remove VLAN</button>
          </div>

        </div>
        </form>
      </div>
    </div>
  </div>


  <div class="modal fade" id="sw_modal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel"
    aria-hidden="true">
    <div class="modal-dialog" role="document">
      <div class="modal-content">
        <div class="modal-header text-center">
          <div id="form-messages"></div>
          <h4 class="modal-title w-100 font-weight-bold">change Switchport Settings</h4>
          <button type="button" class="close" data-dismiss="modal" aria-label="Close">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        <form  method="get" action="/swconfChange/">
        {% csrf_token %}
        <div class="modal-sw">
          <div class="md-form mb-5">

              <input type="hidden" class="form-control" name="int_id" id="int_id">
          </div>

          <div class="md-form mb-5">
            <label data-error="wrong" data-success="right" for="form29">Switchport Mode</label><br>
            <input type="radio" id="native" name="mode" value="native">
            <label>Native</label><br>
            <input type="radio" id="access" name="mode" value="access">
            <label>Access</label>
            <input type="radio" id="trunk" name="mode" value="trunk">
            <label>Trunk</label>
          </div>
          <div class="md-form mb-5">
            <label>Vlan Numbers</label>
              <input type="text" class="form-control" name="sw_vlan" placeholder="E.g: 10 OR 10,20">
          </div>
          <div class="md-form mb-5">
            <button type="submit" class="btn btn-primary" name="submit">Save</button>

          </div>

        </div>
        </form>
      </div>
    </div>
  </div>







<!-- {% for ver in version %}
<h1 class="h3 mb-2 text-gray-800" id="routerinfo">{{ver.hostname}}</h1>
{%endfor%} -->
<div class="" id="routerinfo">

</div>

<!-- For breaking the lines and printing exact output -->
<div class="d-flex justify-content-between">
<div class="p-2">
  <div class="tab">
    <button id="route" class="tablinks" onclick="openCity(event, 'London')">VLAN Table</button>
    <button class="tablinks" onclick="openCity(event, 'Paris')">Spanning tree</button>
    <button class="tablinks" onclick="openCity(event, 'Tokyo')">Trunk Status</button>
    <button class="tablinks" onclick="openCity(event, 'Pokhara')">Switchport</button>
    <button class="tablinks" onclick="openCity(event, 'Kathmandu')">Configure</button>
  </div>

  <div id="London" class="tabcontent">
    <div class="table-responsive">
      <table class="table table-bordered" id="dataTable" width="100%" cellspacing="0">
        <thead>
          <tr>
            <th>VLAN ID</th>
            <th>NAME</th>
            <th>INTERFACES</th>


          </tr>
        </thead>

        <tbody id="vlanBody">


        </tbody>
      </table>
    </div>
    <h5>Add VLAN</h5>
    <form class="form-inline col-md-offset-2 col-md-7" method="get" action="/swconfChange/">
      {% csrf_token %}
        <div class="form-group">

            <input type="text" class="form-control" name="vlan_id" placeholder="VLAN ID">
        </div>
        <div class="form-group">

            <input type="text" class="form-control" name="vlan_name" placeholder="VLAN Name">
        </div>
        <button type="submit" class="btn btn-primary" name="submit">Save</button>
    </form>
  </div>

  <div id="Paris" class="tabcontent">

  </div>

  <div id="Tokyo" class="tabcontent">

  </div>
  <div id="Pokhara" class="tabcontent">
    <div class="table-responsive">
      <table class="table table-bordered" id="spanTable" width="100%" cellspacing="0">
        <thead>
          <tr>
            <th>INTERFACE</th>
            <th>MODE</th>
            <th>ACCESS VLAN</th>
            <th>NATIVE VLAN</th>
            <th>Trunk</th>


          </tr>
        </thead>

        <tbody id="vlanBody">


        </tbody>
      </table>
  </div>
  <div id="Kathmandu" class="tabcontent">

    <form class="form-horizontal" action="/swconfChange/" method="get">
      {% csrf_token %}
    <div class="form-group">
      <label class="control-label col-sm-2" for="email">Hostname:</label>
      <div class="col-sm-10">
        <input type="text" class="form-control" placeholder="Enter hostname" name="hostname">
      </div>
    </div>
    <div class="form-group">
      <label class="control-label col-sm-2" for="pwd">Command:</label>
      <div class="col-sm-10">
        <input type="text" class="form-control"  placeholder="One Command to be executed in config mode" name="olc">
      </div>
    </div>

    <div class="form-group">
      <div class="col-sm-offset-2 col-sm-10">
        <button type="submit" class="btn btn-primary" name="submit">Submit</button>
      </div>
    </div>
  </form>
  </div>
</div>

<div class="p-2">
  <!-- DataTales Example -->
  <div class="card shadow mb-4">
    <div class="card-header py-3">
      <h6 class="m-0 font-weight-bold text-primary">Interfaces</h6>
    </div>
    <div class="card-body">
      <div class="table-responsive">
        <table class="table table-bordered" id="dataTable" width="100%" cellspacing="0">
          <thead>
            <tr>
              <th>Interfaces</th>
              <th>IP address</th>
              <th>Link Status</th>
              <th>Protocol Status</th>

            </tr>
          </thead>

          <tbody id="tablebody">


          </tbody>
        </table>
      </div>
    </div>
  </div>
</div>
</div>
</div>

<style>


/* Style the tab */
.tab {
  overflow: hidden;
  border: 1px solid #ccc;
  background-color: #f1f1f1;

}

/* Style the buttons inside the tab */
.tab button {
  background-color: inherit;
  float: left;
  border: none;
  outline: none;
  cursor: pointer;
  padding: 14px 16px;
  transition: 0.3s;
  font-size: 17px;
}

/* Change background color of buttons on hover */
.tab button:hover {
  background-color: #ddd;
}

/* Create an active/current tablink class */
.tab button.active {
  background-color: #ccc;
}

/* Style the tab content */
.tabcontent {
  display: none;
  padding: 6px 12px;
  border: 1px solid #ccc;
  border-top: none;
}
</style>

{% endblock content %}
