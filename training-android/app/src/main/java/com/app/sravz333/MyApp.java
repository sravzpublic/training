package com.app.sravz333;

import android.app.Application;
import android.content.Intent;
import android.os.Build;
import android.os.Handler;
import android.os.StrictMode;

import com.app.sravz333.util.LogUtil;
import com.google.android.gms.ads.MobileAds;
import com.onesignal.Continue;
import com.onesignal.OneSignal;
import org.json.JSONObject;

import java.lang.reflect.Method;

public class MyApp extends Application {

    @Override
    public void onCreate() {
        super.onCreate();
        MobileAds.initialize(this);
        OneSignal.initWithContext(this,"7d07cbc5-375c-4f4b-9d7d-cf185a16d492x");
        OneSignal.getNotifications().requestPermission(true, Continue.none());

        OneSignal.getNotifications().addClickListener(result -> {
            result.getNotification().getTitle();
            LogUtil.loge("notificationOpened");
            LogUtil.loge("title: "+result.getNotification().getTitle());
            LogUtil.loge("body: "+result.getNotification().getBody());
            LogUtil.loge("launchUrl: "+result.getNotification().getLaunchURL());
            JSONObject data = result.getNotification().getAdditionalData();
            String customKey;
            if (data != null) {
                customKey = data.optString("customkey", "");
                if (!customKey.equals(""))
                    LogUtil.loge("customkey set with value: " + customKey);
                else
                    LogUtil.loge("customkey null");
            }
            sendBroadcast(new Intent("close"));
            new Handler().postDelayed(new Runnable() {
                @Override
                public void run() {
                    Intent intent = new Intent(MyApp.this, Home.class);
                    intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
                    if(result.getNotification().getLaunchURL() != null)
                        intent.putExtra("launchURL", result.getNotification().getLaunchURL());
                    startActivity(intent);
                }
            }, 500);
        });

//        OneSignal.getNotifications().      .setNotificationOpenedHandler(new OneSignal.NotificationOpenedHandler() {
//                    @Override
//                    public void notificationOpened(final OSNotificationOpenResult result) {
//                        LogUtil.loge("notificationOpened");
//                        LogUtil.loge("title: "+result.notification.payload.title);
//                        LogUtil.loge("body: "+result.notification.payload.body);
//                        LogUtil.loge("launchUrl: "+result.notification.payload.launchURL);
//                        JSONObject data = result.notification.payload.additionalData;
//                        String customKey;
//                        if (data != null) {
//                            customKey = data.optString("customkey", null);
//                            if (customKey != null)
//                                LogUtil.loge("customkey set with value: " + customKey);
//                            else
//                                LogUtil.loge("customkey null");
//                        }
//                        sendBroadcast(new Intent("close"));
//                        new Handler().postDelayed(new Runnable() {
//                            @Override
//                            public void run() {
//                                Intent intent = new Intent(MyApp.this, Home.class);
//                                intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
//                                if(result.notification.payload.launchURL != null)
//                                    intent.putExtra("launchURL", result.notification.payload.launchURL);
//                                startActivity(intent);
//                            }
//                        }, 500);
//                    }
//                })
//                .init();

        if(Build.VERSION.SDK_INT>=24){
            try{
                Method m = StrictMode.class.getMethod("disableDeathOnFileUriExposure");
                m.invoke(null);
            }
            catch(Exception e){
                e.printStackTrace();
            }
        }
    }
}
