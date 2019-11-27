import React, { Component } from 'react';
import PushNotification from 'react-native-push-notification';

export default class NotifyService {
  constructor(onNotification) {
    this.configure(onNotification);
    this.lastId = 0;
  }

  configure(onNotification) {
    PushNotification.configure({
      onNotification: onNotification,
      popInitialNotification: true,
    });
  }

  localNotify(msg) {
  	this.lastId++;
	PushNotification.localNotification({
		message: msg,
	});
  }

  scheduleNotify(interval, msg) {
  	this.lastId++;
	PushNotification.localNotificationSchedule({
		date: new Date(Date.now() + (interval * 1000)),
		repeatType: 'minute',
		message: msg,
		largeIcon: "ic_launcher",
	});
  }

  checkPermission(cbk) {
    return PushNotification.checkPermissions(cbk);
  }

  cancelNotif() {
    PushNotification.cancelLocalNotifications({id: ''+this.lastId});
  }

  cancelAll() {
    PushNotification.cancelAllLocalNotifications();
  }
}