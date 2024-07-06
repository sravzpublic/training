package com.app.sravz33.util;

import android.os.Handler;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import com.app.sravz33.Home;
import com.app.sravz33.Settings;
import com.bumptech.glide.Glide;

public class GifUtil {

    public static void showGifAnimation(final Home activity, final ViewGroup gifAnim, final ImageView gifAnimImg){
        gifAnim.setVisibility(View.VISIBLE);
        Glide.with(activity).load(Settings.GIF_NAME).into(gifAnimImg);
        new Handler().postDelayed(new Runnable() {
            @Override
            public void run() {
                LogUtil.loge("hide gif");
                gifAnim.setVisibility(View.GONE);
                if(!Home.homeLoaded){
                    activity.showProgress();
                }
            }
        }, (Settings.GIF_LOAD_MAX_SECONDS+1) * 1000);
    }

    public static void hideGifAnimation(final ViewGroup gifAnim){
        gifAnim.setVisibility(View.GONE);
    }
}
