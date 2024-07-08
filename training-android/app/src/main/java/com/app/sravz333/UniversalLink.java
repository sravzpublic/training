package com.app.sravz333;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;

import com.app.sravz333.util.LogUtil;

public class UniversalLink extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_universal_link);

        LogUtil.loge("UniversalLink");
        finishAffinity();
        Intent home = new Intent(this, Home.class);
        home.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TASK |Intent.FLAG_ACTIVITY_CLEAR_TOP);
        home.setData(getIntent().getData());
        startActivity(home);
    }
}
