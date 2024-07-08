package com.app.sravz333.util;

import android.content.Context;
import android.content.SharedPreferences;
import com.app.sravz333.Settings;
import com.onesignal.Continue;
import com.onesignal.OneSignal;

public class PrefsUtil {
    private static final String name = "com.app.sravz333";

    private static SharedPreferences getSharedPrefs(Context context){
        return context.getSharedPreferences(name, Context.MODE_PRIVATE);
    }

    private static final String AppLanuches = "AppLanuches3";
    public static void setAppLanuches(Context context, int i){
        SharedPreferences sp = getSharedPrefs(context);
        sp.edit().putInt(AppLanuches, i).apply();
    }
    public static int getAppLanuches(Context context){
        SharedPreferences sp = getSharedPrefs(context);
        return sp.getInt(AppLanuches, 0);
    }

    private static final String NoThanksPressed = "NoThanksPressed3";
    public static void setNoThanksPressed(Context context, boolean b){
        SharedPreferences sp = getSharedPrefs(context);
        sp.edit().putBoolean(NoThanksPressed, b).apply();
    }
    public static boolean isNoThanksPressed(Context context){
        SharedPreferences sp = getSharedPrefs(context);
        return sp.getBoolean(NoThanksPressed, false);
    }

    private static final String RateNowPressed = "RateNowPressed3";
    public static void setRateNowPressed(Context context, boolean b){
        SharedPreferences sp = getSharedPrefs(context);
        sp.edit().putBoolean(RateNowPressed, b).apply();
    }
    public static boolean isRateNowPressed(Context context){
        SharedPreferences sp = getSharedPrefs(context);
        return sp.getBoolean(RateNowPressed, false);
    }

    private static final String PushEnabled = "PushEnabled";
    public static void setPushEnabled(Context context, boolean b){
        SharedPreferences sp = getSharedPrefs(context);
        sp.edit().putBoolean(PushEnabled, b).apply();
        Settings.PUSH_ENABLED = b;
        OneSignal.getNotifications().requestPermission(b, Continue.none());
        OneSignal.setConsentGiven(b);
    }
    public static boolean isPushEnabled(Context context){
        SharedPreferences sp = getSharedPrefs(context);
        return sp.getBoolean(PushEnabled, Settings.PUSH_ENABLED);
    }


}