package com.app.myapplication;

import android.app.PendingIntent;
import android.content.Intent;
import android.graphics.drawable.Drawable;
import android.net.Uri;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import java.util.ArrayList;
import java.util.List;
import android.app.Activity;
import android.os.Bundle;
import android.telephony.SmsManager;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.CompoundButton;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.Spinner;
import android.widget.Switch;
import android.widget.TextView;
import android.widget.Toast;

public class MainActivity extends AppCompatActivity {


    private Button btnSubmit;
    private EditText quantity;
    private ImageView nachani;
    private ImageView jeera;
    private ImageView khichadi;
    private ImageView methi;
    private String flavour;
    private Switch aSwitch;
    private String action="Delete";

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        addListenerOnButton();
    }

    // get the selected dropdown list value
    public void addListenerOnButton() {


        btnSubmit = (Button) findViewById(R.id.submit);
        quantity=(EditText) findViewById(R.id.quantity);
        nachani=(ImageView)findViewById(R.id.nachani);
        jeera=(ImageView)findViewById(R.id.jeera);
        khichadi=(ImageView)findViewById(R.id.khichadi);
        methi=(ImageView)findViewById(R.id.methi);
        aSwitch=(Switch)findViewById(R.id.addDdelete);


        nachani.setOnClickListener(new OnClickListener() {
            @Override
            public void onClick(View v) {
                flavour="Nachani";
            }
        });

        jeera.setOnClickListener(new OnClickListener() {
            @Override
            public void onClick(View v) {
                flavour="Jeera";
            }
        });

        khichadi.setOnClickListener(new OnClickListener() {
            @Override
            public void onClick(View v) {
                flavour="Khicahdi";
            }
        });

        methi.setOnClickListener(new OnClickListener() {
            @Override
            public void onClick(View v) {
                flavour="Methi";
            }
        });

        aSwitch.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {

                if(isChecked)
                    action="Add";
                else
                    action="Delete";
            }
        });

        btnSubmit.setOnClickListener(new OnClickListener() {

            @Override
            public void onClick(View v) {


                if(action.equals("Add"))
                {
                    Intent intent = new Intent(Intent.ACTION_VIEW, Uri.parse("sms:" +"7498938999" ));
                    intent.putExtra("sms_body","Shranisa Khakara Order : Add To Inventory \n Khakara Flavour : "+flavour+"\n"+"Quantity : "+quantity.getText());
                    startActivity(intent);
                }
                else
                {
                    Intent intent = new Intent(Intent.ACTION_VIEW, Uri.parse("sms:" +"7498938999" ));
                    intent.putExtra("sms_body"," Shranisa Khakara Order : Delete From Inventory\n Khakara Flavour : "+flavour+"\n"+"Quantity : "+quantity.getText());
                    startActivity(intent);
                }
            }
        });
    }
}
