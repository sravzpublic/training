package com.app.sravz333.util;

import static android.content.ContentValues.TAG;

import android.util.Log;
import android.view.ViewGroup;
import android.widget.RelativeLayout;

import androidx.annotation.NonNull;

import com.app.sravz333.Home;
import com.app.sravz333.R;
import com.app.sravz333.Settings;
import com.google.android.gms.ads.AdRequest;
import com.google.android.gms.ads.AdSize;
import com.google.android.gms.ads.AdView;
import com.google.android.gms.ads.LoadAdError;
import com.google.android.gms.ads.interstitial.InterstitialAd;
import com.google.android.gms.ads.interstitial.InterstitialAdLoadCallback;

public class AdUtil {

    public static void loadBannerAd(Home activity, ViewGroup adParent) {
        if(Settings.BANNER_AD){
            adParent.removeAllViews();
            AdRequest adRequest = new AdRequest.Builder().build();
            AdView adView = new AdView(activity);
            adView.setAdSize(AdSize.SMART_BANNER);
            adView.setAdUnitId(activity.getResources().getString(R.string.admobBannerId));
            adView.setBackgroundColor(activity.getResources().getColor(android.R.color.transparent));
            adView.loadAd(adRequest);
            RelativeLayout.LayoutParams params = new RelativeLayout.LayoutParams(RelativeLayout.LayoutParams.WRAP_CONTENT, RelativeLayout.LayoutParams.WRAP_CONTENT);
            params.addRule(RelativeLayout.ALIGN_BOTTOM, RelativeLayout.TRUE);
            adParent.addView(adView, params);
        }
    }

    public static void loadInterstitialAd(Home activity){
        LogUtil.loge("loadInterstitialAd");
        Home.linkClicks = 0;
        if(Settings.INTERSTITIAL_AD){
            AdRequest adRequest = new AdRequest.Builder().build();

            InterstitialAd.load(activity, String.valueOf(R.string.admobInterstitialId), adRequest,
                    new InterstitialAdLoadCallback() {
                        @Override
                        public void onAdLoaded(@NonNull InterstitialAd interstitialAd) {
                            LogUtil.loge("onAdLoaded");
                            super.onAdLoaded(interstitialAd);
                            interstitialAd.show(activity);
                        }

                        @Override
                        public void onAdFailedToLoad(@NonNull LoadAdError loadAdError) {
                            // Handle the error
                            Log.d(TAG, loadAdError.toString());

                        }
                    });
//            mInterstitialAd.setAdUnitId(activity.getResources().getString(R.string.admobInterstitialId));
//            mInterstitialAd.loadAd(new AdRequest.Builder().build());
//            mInterstitialAd.setAdListener(new AdListener(){
//                @Override
//                public void onAdLoaded() {
//                    LogUtil.loge("onAdLoaded");
//                    super.onAdLoaded();
//                    mInterstitialAd.show();
//                }
//            });
        }
    }
}