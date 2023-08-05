import 'package:flutter/material.dart';
import 'package:flutter_bluetooth_serial/flutter_bluetooth_serial.dart';
import 'package:servo_app/connection.dart';
import 'package:servo_app/led.dart';

import 'dart:async';
import 'dart:convert';
import 'dart:typed_data';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bluetooth_serial/flutter_bluetooth_serial.dart';
import 'package:control_button/control_button.dart';
import 'package:http/http.dart' as http;
import 'dart:convert' as convert;
import 'dart:io';
import 'dart:math' as math;

import 'package:path/path.dart' as Path;
//import 'dart:html';

//var R= await sendDataStop('http://172.28.132.146:8000/name?') as Map <String, dynamic>;


// 1 Manual
// 0 Automatic

MaualControl(String url)
async{

  http.Response response=await http.post(Uri.parse(url),body: convert.json.encode({ 'name':'1'}));
  //return  convert.json.decode(response.body) ;

}



AutomaticControl(String url)
async{

  http.Response response=await http.post(Uri.parse(url),body: convert.json.encode({'name':'0'}));
  //return  convert.json.decode(response.body) ;

}



void main() {
  runApp(Main_page());
}

class Main_page extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      theme: ThemeData.dark(),
      debugShowCheckedModeBanner: false,
      home: Modes(),
    );
  }
}

class Modes extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        centerTitle: true,
        title: Text('Flutter Car Controller', style: TextStyle(fontSize: 30)),
      ),
      body: Stack(children: [
        Padding(
            padding: EdgeInsets.only(top: 200),
            child: Container(
              width: double.infinity,
              height: 150.0,
              child: RaisedButton(
                child: Text(
                  'Manual',
                  style: TextStyle(fontSize: 30),
                ),
                onPressed: ()  {
                  //await MaualControl('http://192.168.43.88:5635/mode?mode=1') as Map <String, dynamic>;


                  Navigator.push(
                    context,
                    MaterialPageRoute(builder: (context) => MyApp()),

                  );
                },
              ),
            )),
        Padding(
            padding: EdgeInsets.only(top: 400),
            child: Container(
              width: double.infinity,
              height: 150.0,
              child: RaisedButton(
                child: Text(
                  'Automatic',
                  style: TextStyle(fontSize: 30),
                ),
                onPressed: () {

                  //await AutomaticControl('http://192.168.43.88:5635/mode?mode=1') as Map <String, dynamic>;



                  Navigator.push(
                    context,
                    MaterialPageRoute(builder: (context) => Automatic()),
                  );
                },
              ),
            ))
      ]),
    );
  }
}

class Automatic extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        centerTitle: true,
        title: Text('Auto_control', style: TextStyle(fontSize: 30)),
      ),
      body: Stack(children: [
        Padding(
            padding: EdgeInsets.only(top: 200),
            child: Container(
              width: double.infinity,
              height: 150.0,
              child: RaisedButton(
                child: Text(
                  'ON',
                  style: TextStyle(fontSize: 30),
                ),
                color: Colors.green,
                onPressed: () {},
              ),
            )),
        Padding(
            padding: EdgeInsets.only(top: 400),
            child: Container(
              width: double.infinity,
              height: 150.0,
              child: RaisedButton(
                child: Text(
                  'OFF',
                  style: TextStyle(fontSize: 30),
                ),
                color: Colors.red,
                onPressed: () {},
              ),
            ))
      ]),
    );
  }
}

class MyApp extends StatelessWidget {
  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      // appBar: AppBar(
      //   centerTitle: true,
      //   title: Text('Flutter Car Controller'),
      // ),
      body: FutureBuilder(
        future: FlutterBluetoothSerial.instance.requestEnable(),
        builder: (context, future) {
          if (future.connectionState == ConnectionState.waiting) {
            return Scaffold(
              body: Container(
                height: double.infinity,
                child: Center(
                  child: Icon(
                    Icons.bluetooth_disabled,
                    size: 200.0,
                    color: Colors.black12,
                  ),
                ),
              ),
            );
          } else {
            return Home();
          }
        },
        // child: MyHomePage(title: 'Flutter Demo Home Page'),
      ),
    );
  }
}

class Home extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return SafeArea(
        child: Scaffold(
      appBar: AppBar(
        centerTitle: true,
        title: Text('Connection', style: TextStyle(fontSize: 30)),
      ),
      body: SelectBondedDevicePage(
        onCahtPage: (device1) {
          BluetoothDevice device = device1;
          Navigator.push(
            context,
            MaterialPageRoute(
              builder: (context) {
                return ChatPage(server: device);
              },
            ),
          );
        },
      ),
    ));
  }
}
