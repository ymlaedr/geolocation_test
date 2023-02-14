#!/bin/bash



## --------------------------------------------------------------------------
## 定数定義
## --------------------------------------------------------------------------

PRJ_DIR=$(cd $(dirname ${BASH_SOURCE:-$0}); pwd);

PYTHON_EXEC_IMAGE='3.11.1-alpine3.17';

EXEC_SCRIPT_SSL_GEN="\
	apk add \
	  --no-cache \
	  --update-cache \
	  --virtual .exec_sslgen_dependencies \
	    openssl \
	 && \
	openssl genrsa -out server.key \
	 && \
	openssl req -new -key server.key -out server.csr -subj '/C=JP/ST=Tokyo/L=Minato City/O=TeX2e/CN=mytest.example.com' \
	 && \
	echo 'subjectAltName = DNS:mytest.example.com, IP:192.168.0.169' > san.txt \
	 && \
	openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt -extfile san.txt \
	 && \
	openssl x509 -text -in server.crt -noout";
PRE_EXEC_SCRIPT_AARCH64="\
	apk add \
	  --no-cache \
	  --update-cache \
	  --virtual .exec_pip_dependencies \
	    alpine-sdk \
	    musl-dev \
	    libffi-dev \
	 && \
	apk add \
	  --no-cache \
	  --update-cache \
	  --virtual .install_pip_requirements_dependencies \
	    openssl \
	    alpine-sdk";
PRE_EXEC_SCRIPT="\
	pip install --upgrade pip \
	 && \
	pip install -r requirements.txt";
POST_EXEC_SCRIPT="\
	apk del --purge .exec_sslgen_dependencies";
POST_EXEC_SCRIPT_AARCH64="\
	apk del --purge .install_pip_requirements_dependencies";
[ "$(arch)" = 'aarch64' ] && PRE_EXEC_SCRIPT="\
	${PRE_EXEC_SCRIPT_AARCH64} \
	 && \
	${PRE_EXEC_SCRIPT} \
	 && \
	${POST_EXEC_SCRIPT_AARCH64}";
EXEC_SCRIPT_APP="${PRE_EXEC_SCRIPT} && python app.py";
EXEC_SCRIPT_SH="${PRE_EXEC_SCRIPT} && sh";
EXEC_SCRIPT_DB_UPGRADE="${PRE_EXEC_SCRIPT} && flask db upgrade";



## --------------------------------------------------------------------------
## 開発に使用するコマンドの定義
## --------------------------------------------------------------------------

## Docker 起動のための共通処理
_exec() {
	docker run --rm \
		-p '8080:8080' \
		-e "FLASK_APP=app.py" \
		-v "${PRJ_DIR}:/geolocation_test" \
		--workdir "/geolocation_test" \
		-it python:${PYTHON_EXEC_IMAGE} \
			sh "${@}";
}

exec_ssl_gen() { _exec -c "${EXEC_SCRIPT_SSL_GEN}"; }

## Docker で flask db upgrade を実行
exec_db_upgrade() { _exec -c "${EXEC_SCRIPT_DB_UPGRADE}"; }

## Docker で app.py を起動
exec_app() { _exec -c "${EXEC_SCRIPT_APP}"; }

## Docker で開発環境のシェルを起動
exec_sh() { _exec -c "${EXEC_SCRIPT_SH}"; }

download_statics() {
	declare -A ESM_JS_LIST=(
		['socket.io.esm.min.js']='https://cdn.socket.io/4.3.2/socket.io.esm.min.js'
		['vue.esm-browser.js']='https://unpkg.com/vue@3.2.47/dist/vue.esm-browser.js'
		['socket.io.esm.min.js.map']='http://cdn.socket.io/4.5.3/socket.io.esm.min.js.map'
	);

	for ESM_JS in ${!ESM_JS_LIST[@]};
	do
		curl --output "${PRJ_DIR}/static/${ESM_JS}" ${ESM_JS_LIST[${ESM_JS}]}
	done
}