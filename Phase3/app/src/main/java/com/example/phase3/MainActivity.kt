package com.example.phase3
//import android.content.Intent
//import android.graphics.Bitmap
//import android.provider.MediaStore
//import android.widget.Button
//import android.widget.ImageView
//import kotlinx.android.synthetic.main.activity_take_photo.*
//import androidx.core.app.ComponentActivity.ExtraData
//import androidx.core.content.ContextCompat.getSystemService
//import android.icu.lang.UCharacter.GraphemeClusterBreak.T
//import sun.jvm.hotspot.utilities.IntArray
import android.content.Context
import android.content.Intent
import android.opengl.Visibility
import android.os.Bundle
import android.util.Log
import android.view.View
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.fragment.app.FragmentActivity
import com.google.android.gms.auth.api.signin.GoogleSignIn
import com.google.android.gms.auth.api.signin.GoogleSignInAccount
import com.google.android.gms.auth.api.signin.GoogleSignInClient
import com.google.android.gms.auth.api.signin.GoogleSignInOptions
import com.google.android.gms.common.SignInButton
import com.google.android.gms.common.api.ApiException
import com.google.android.gms.tasks.Task
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.auth.GoogleAuthProvider
import kotlinx.android.synthetic.main.activity_main.*

//import androidx.core.app.ActivityCompat.startActivityForResult
//import androidx.core.app.ComponentActivity.ExtraData
//import androidx.core.content.ContextCompat.getSystemService
//import android.icu.lang.UCharacter.GraphemeClusterBreak.T
//import sun.jvm.hotspot.utilities.IntArray

class MainActivity : AppCompatActivity() {

    val RC_SIGN_IN: Int = 1
    lateinit var mGoogleSignInClient: GoogleSignInClient
    lateinit var mGoogleSignInOptions: GoogleSignInOptions
    private lateinit var firebaseAuth: FirebaseAuth

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val gso = GoogleSignInOptions.Builder(GoogleSignInOptions.DEFAULT_SIGN_IN)
            .requestEmail()
            .build()
        val mGoogleSignInClient = GoogleSignIn.getClient(this, gso)

        sign_in_button.visibility=View.VISIBLE
        sign_in_button.setSize(SignInButton.SIZE_STANDARD)
        sign_in_button.setOnClickListener {
            val signInIntent = mGoogleSignInClient.getSignInIntent()
            startActivityForResult(signInIntent, RC_SIGN_IN)
        }
    }

    fun viewCategories(view:View) {
        val viewCatIntent = Intent(this, ViewCategoriesActivity::class.java)
        startActivity(viewCatIntent)
    }

    fun signOutOnClick(view:View){
        startActivity(MainActivity.getLaunchIntent(this))
        FirebaseAuth.getInstance().signOut()
        sign_in_button.visibility=View.VISIBLE
        layout_buttons.visibility=View.GONE
    }

    companion object {
        fun getLaunchIntent(from: Context) = Intent(from, MainActivity::class.java).apply {
            addFlags(Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK)
        }
    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        Log.d("debug", resultCode.toString() + " vs " + RC_SIGN_IN.toString() + ", compare:" + (requestCode == RC_SIGN_IN).toString())
        if (requestCode == RC_SIGN_IN) {
            var task :Task<GoogleSignInAccount> = GoogleSignIn.getSignedInAccountFromIntent(data)
            handleSignInResult(task)
        }
    }

    private fun handleSignInResult(completedTask : Task<GoogleSignInAccount>){
        try{
            sign_in_button.visibility=View.GONE
            layout_buttons.visibility=View.VISIBLE
            val account = completedTask.getResult(ApiException::class.java)
            welcome_title.text= account!!.displayName
            welcome_title.text="Hello! " + account.displayName
        } catch (e:ApiException){
            Log.d("exception","Login failed due to:" + e.message)
        }
    }



}
