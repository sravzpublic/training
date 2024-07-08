package com.app.sravz333.util;

import android.os.Handler;
import android.webkit.WebView;

public class TimerUtil {
    Handler handler;
    Runnable runnable;

    public void startTimer(final WebView webView) {
        handler = new Handler();
        runnable = new Runnable() {
            @Override
            public void run() {
                webView.loadUrl("javascript: Android.findCurrentUrl(window.location.href)");
                handler.postDelayed(runnable, 1000);
            }
        };
        handler.postDelayed(runnable, 1000);
    }

    public void stopTimer(){
        if(handler != null){
            handler.removeCallbacks(runnable);
            handler = null;
        }
    }

}
