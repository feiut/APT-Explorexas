package com.example.phase3

import android.content.Intent
import android.net.Uri
import android.os.Build.VERSION_CODES.M
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.os.Environment
import android.provider.MediaStore
import java.io.File
import java.io.IOException

class CreateReportActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_create_report)
    }

    private fun camera() = try{
        var tempImg1 = File(Environment.getExternalStorageDirectory(), System.currentTimeMillis() + ".jpg")
        if (!tempImg1.exists()){
            var b = tempImg1.createNewFile();
            if (b){
                println(tempImg1.getAbsolutePath())
                var intent = Intent(MediaStore.ACTION_IMAGE_CAPTURE)
                intent.putExtra(MediaStore.EXTRA_OUTPUT, Uri.fromFile(tempImg1))
                startActivityForResult(intent, 1)
            }else{
                print(b)
            }
        }else{
            print(tempImg1)
        }
    }catch(e : IOException){
        println(e)
    }
}
