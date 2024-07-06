package com.app.sravz33.util;

import android.app.Activity;
import android.widget.Toast;

import androidx.annotation.Nullable;

import com.android.billingclient.api.AcknowledgePurchaseParams;
import com.android.billingclient.api.AcknowledgePurchaseResponseListener;
import com.android.billingclient.api.BillingClient;
import com.android.billingclient.api.BillingClientStateListener;
import com.android.billingclient.api.BillingFlowParams;
import com.android.billingclient.api.BillingResult;
import com.android.billingclient.api.Purchase;
import com.android.billingclient.api.PurchasesUpdatedListener;
import com.android.billingclient.api.SkuDetails;
import com.android.billingclient.api.SkuDetailsParams;
import com.android.billingclient.api.SkuDetailsResponseListener;
import com.app.sravz33.Settings;

import java.util.Arrays;
import java.util.List;

/*
    implementation 'com.android.billingclient:billing:2.0.3'
    <uses-permission android:name="com.android.vending.BILLING" />
 */

public class InAppBilling {
    Activity context;
    BillingClient billingClient;
    List<SkuDetails> skuDetailsList;
    List<String> skuList =  Arrays.asList(Settings.IN_APP_BILLING_PRODUCT_IDS);
    SkuDetails skuDetails;

    public void setupBillingClient(final Activity context){
        this.context = context;
        billingClient = BillingClient.newBuilder(context)
                .enablePendingPurchases()
                .setListener(new PurchasesUpdatedListener() {
                    @Override
                    public void onPurchasesUpdated(BillingResult billingResult, @Nullable List<Purchase> purchases) {
                        LogUtil.loge("onPurchasesUpdated");
                        if (billingResult.getResponseCode() == BillingClient.BillingResponseCode.OK && purchases != null) {
                            // Purchase Done
                            for (Purchase purchase : purchases) {
                                acknowledgePurchase(purchase.getPurchaseToken());
                            }
                        }
                        else {
                            // Handle any other error codes.
                            Toast.makeText(context, "Purchase Failed!", Toast.LENGTH_SHORT).show();
                        }
                    }
                })
                .build();
        billingClient.startConnection(new BillingClientStateListener() {
            @Override
            public void onBillingSetupFinished(BillingResult billingResult) {
                LogUtil.loge("onBillingSetupFinished");
                if (billingResult.getResponseCode() == BillingClient.BillingResponseCode.OK) {
                    LogUtil.loge("The BillingClient is setup successfully");
                    loadAllSKUs();
                }
            }
            @Override
            public void onBillingServiceDisconnected() {
                LogUtil.loge("onBillingServiceDisconnected");
            }
        });
    }

    private void loadAllSKUs() {
        if(billingClient.isReady()){
            SkuDetailsParams params = SkuDetailsParams.newBuilder()
                    .setSkusList(skuList)
                    .setType(BillingClient.SkuType.INAPP)
                    .build();
            billingClient.querySkuDetailsAsync(params, new SkuDetailsResponseListener() {
                @Override
                public void onSkuDetailsResponse(BillingResult billingResult, List<SkuDetails> skuDetailsList) {
                    LogUtil.loge("onSkuDetailsResponse");
                    InAppBilling.this.skuDetailsList = skuDetailsList;
                    for (SkuDetails skuDetails : skuDetailsList) {
                        LogUtil.loge("sku: "+skuDetails.getSku());
                        LogUtil.loge("price: "+skuDetails.getPrice());
                        LogUtil.loge("currency: "+skuDetails.getPriceCurrencyCode());
                    }
                }
            });
        }
        else{
            LogUtil.loge("billingClient not ready");
        }
    }

    public void makePurchase(String productId){
        if(skuDetailsList.size() == 0)
            return;
        for (SkuDetails details : skuDetailsList) {
            if(details.getSku().equals(productId)){
                skuDetails = details;
            }
        }
        if(skuDetails == null){
            return;
        }
        LogUtil.loge("makePurchase: "+skuDetails.getSku());
        BillingFlowParams billingFlowParams = BillingFlowParams.newBuilder()
                .setSkuDetails(skuDetails)
                .build();
        billingClient.launchBillingFlow(context, billingFlowParams);
    }

    private void acknowledgePurchase(String purchaseToken) {
        AcknowledgePurchaseParams params = AcknowledgePurchaseParams.newBuilder()
                .setPurchaseToken(purchaseToken)
                .build();
        billingClient.acknowledgePurchase(params, new AcknowledgePurchaseResponseListener() {
            @Override
            public void onAcknowledgePurchaseResponse(BillingResult billingResult) {
                LogUtil.loge("onAcknowledgePurchaseResponse");
                int responseCode = billingResult.getResponseCode();
                String debugMessage = billingResult.getDebugMessage();
                LogUtil.loge("responseCode: "+responseCode);
                LogUtil.loge("debugMessage: "+debugMessage);
            }
        });
    }
}
