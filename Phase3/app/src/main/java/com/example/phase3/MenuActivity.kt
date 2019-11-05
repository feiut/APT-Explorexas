package com.example.phase3

import android.content.Context
import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Log
import android.view.View
import android.widget.Button
import android.widget.TextView
import com.google.android.gms.tasks.OnCompleteListener
import com.google.android.gms.tasks.Task
import com.google.firebase.auth.FirebaseAuth
import kotlinx.android.synthetic.main.activity_main.*
import kotlinx.android.synthetic.main.activity_menu.*
import org.w3c.dom.Text

class MenuActivity : AppCompatActivity() {

    lateinit var clientAccountEmail : String

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val bundle = intent.extras
        setContentView(R.layout.activity_menu)
        var clientAccount = bundle!!.getString("clientAccount") as String
        clientAccountEmail = bundle!!.getString("clientAccountEmail") as String
        hello_title.text= "Hello! " + clientAccount
    }

    fun createReport(view:View){
        val intent = Intent(this, CreateReportActivity::class.java)
        intent.putExtra("clientAccountEmail", clientAccountEmail)
        startActivity(intent)
    }

    fun searchReports(view:View){
        val intent = Intent(this, SearchReportsActivity::class.java)
        startActivity(intent)
    }

    fun viewCategories(view:View) {
        val viewCatIntent = Intent(this, ViewCategoriesActivity::class.java)
        startActivity(viewCatIntent)
    }

    fun viewMaps(view:View){
        val viewMapIntent = Intent(this, MapsActivity::class.java)
        startActivity(viewMapIntent)
    }

    fun signOutOnClick(view:View){
        val viewMainIntent = Intent(this, MainActivity::class.java)
        startActivity(viewMainIntent)
    }
}
