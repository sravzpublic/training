package com.app.sravz33;

import android.content.Context;
import android.graphics.Color;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.core.graphics.drawable.DrawableCompat;

public class MainMenuAdapter extends BaseAdapter {
    private Context mContext;
    private String [] titles;
    private LayoutInflater mLayoutInflater = null;

    public MainMenuAdapter(Context context) {
        mContext = context;
        titles = Settings.DRAWER_TITLES;
        mLayoutInflater = (LayoutInflater) mContext.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
    }
    @Override
    public int getCount() {
        return titles.length;
    }
    @Override
    public Object getItem(int pos) {
        return titles[pos];
    }
    @Override
    public long getItemId(int position) {
        return position;
    }
    @Override
    public View getView(int position, View convertView, ViewGroup parent) {
        View v = convertView;
        CompleteListViewHolder viewHolder;
        if (convertView == null) {
            LayoutInflater li = (LayoutInflater) mContext.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
            v = li.inflate(R.layout.menu_item, null);
            viewHolder = new CompleteListViewHolder(v);
            v.setTag(viewHolder);
        }
        else {
            viewHolder = (CompleteListViewHolder) v.getTag();
        }

        String title = Settings.DRAWER_TITLES[position];
        viewHolder.title.setText(title);
        viewHolder.title.setTextColor(Color.parseColor(Settings.DRAWER_TITLE_COLOR));

        if(!Settings.SHOW_DRAWER_ICONS){
            viewHolder.icon.setVisibility(View.GONE);
        }
        else{
            int icon = Settings.DRAWER_ICONS[position];
            viewHolder.icon.setImageResource(icon);
            viewHolder.icon.setVisibility(View.VISIBLE);
            DrawableCompat.setTint(viewHolder.icon.getDrawable(), Color.parseColor(Settings.DRAWER_ICON_COLOR));
        }

        return v;
    }

    static class CompleteListViewHolder {
        // declare views here
        ImageView icon;
        TextView title;
        public CompleteListViewHolder(View base) {
            //initialize views here
            icon = base.findViewById(R.id.icon);
            title = base.findViewById(R.id.title);
        }
    }
}