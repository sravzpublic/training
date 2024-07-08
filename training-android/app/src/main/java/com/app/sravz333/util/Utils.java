package com.app.sravz333.util;

import android.annotation.SuppressLint;
import android.app.Activity;
import android.content.ActivityNotFoundException;
import android.content.Context;
import android.content.Intent;
import android.content.pm.ActivityInfo;
import android.content.res.Resources;
import android.net.Uri;
import android.os.Build;
import android.os.Handler;
import android.util.DisplayMetrics;
import android.view.View;
import android.view.Window;
import android.view.WindowManager;
import android.widget.ImageView;

import androidx.core.content.ContextCompat;
import androidx.core.graphics.drawable.DrawableCompat;

import com.app.sravz333.Settings;

public class Utils {

    public static void clickEffect(final View view){
        view.setAlpha(0.5f);
        new Handler().postDelayed(new Runnable() {
            @Override
            public void run() {
                view.setAlpha(1f);
            }
        }, 100);
    }

    public static void changeImageViewColor(Activity activity, ImageView imageView, int color){
        DrawableCompat.setTint(imageView.getDrawable(), ContextCompat.getColor(activity, color));
    }

    public static void changeStatusBarColor(Activity ctx, int color){
        if (Build.VERSION.SDK_INT >= 21) {
            Window window = ctx.getWindow();
            window.clearFlags(WindowManager.LayoutParams.FLAG_TRANSLUCENT_STATUS);
            window.addFlags(WindowManager.LayoutParams.FLAG_DRAWS_SYSTEM_BAR_BACKGROUNDS);
            window.setStatusBarColor(color);
        }
    }

    public static void openUrlInChrome(Activity activity, String url){
        Intent intent = new Intent(Intent.ACTION_VIEW, Uri.parse(url));
        intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
        intent.setPackage("com.android.chrome");
        try {
            activity.startActivity(intent);
        } catch (ActivityNotFoundException ex) {
            // Chrome browser presumably not installed so allow user to choose instead
            intent.setPackage(null);
            activity.startActivity(intent);
        }
    }

    public static float convertDpToPixel(float dp, Context context){
        Resources resources = context.getResources();
        DisplayMetrics metrics = resources.getDisplayMetrics();
        float px = dp * ((float)metrics.densityDpi / DisplayMetrics.DENSITY_DEFAULT);
        return px;
    }

    @SuppressLint("SourceLockedOrientationActivity")
    public static void setScreenOrientation(Activity activity) {
        if(Settings.SCREEN_ORIENTATION == 1)
            activity.setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_SENSOR_PORTRAIT);
        else if(Settings.SCREEN_ORIENTATION == 2)
            activity.setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_SENSOR_LANDSCAPE);
    }
}
