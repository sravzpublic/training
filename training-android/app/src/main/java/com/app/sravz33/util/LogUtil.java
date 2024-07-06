package com.app.sravz33.util;

import android.util.Log;

public class LogUtil {
    private static final String tag = "MyLogger";
    private static final boolean showLogs = true;
    private static StringBuilder builder = new StringBuilder();

    public static void loge(String s){
        if(showLogs)
            Log.e(tag, s);
        if(builder == null)
            builder = new StringBuilder();
        builder.append(s);
        builder.append("\n");
    }
}
